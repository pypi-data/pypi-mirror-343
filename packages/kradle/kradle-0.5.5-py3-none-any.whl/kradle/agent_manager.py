import sys
from flask import Flask, jsonify, request
import socket
import signal
import threading

from flask_cors import CORS
from kradle.models import ChallengeInfo, Observation, InitParticipantResponse, OnEventResponse
from kradle.logger import KradleLogger
from kradle.ssh_tunnel import create_tunnel
from kradle.api.client import KradleAPI
from kradle.api.http import KradleAPIError
from kradle.core import MinecraftAgent
import os
KRADLE_URL = "https://app.kradle.ai"

class AgentManager:
    """
    The agent manager creates a server to expose the agent. It handles the lifecycle
    of creating and managing instances of the provided agent class for each participant
    in a challenge.

    The AgentManager class is a singleton (i.e. the class itself behaves as a single instance).
    """

    _instance = None
    _server = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            cls._instance._agents = {}  # session_id_participant_id -> agent instance
            cls._instance._agent_classes = (
                {}
            )  # username -> {class: agent_class, count: int}
            cls._instance._app = None
            cls._instance.port = None
            cls._instance._api_client = KradleAPI()
            cls._instance._logger = KradleLogger()
            cls._instance._kradle_url = os.getenv("KRADLE_URL") or KRADLE_URL
        return cls._instance

    def _is_port_available(self, host: str = "localhost", port: int = 8080):
        try:
            # print(f"checking if port {port} is available on {host}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                # print(f"port {port} is available on {host}")
                return True
        except OSError:
            # print(f"port {port} is not available on {host}")
            return False

    def _setup_server(self, host: str = "localhost", port: int = 8080, debug: bool = False) -> None:
        """Set up and start the server."""
        try:
            thread = threading.Thread(target=lambda: self._app.run(host=host, port=port, debug=debug, use_reloader=False))

            # setting this removes the warnings about the leaked semaphore objects at shutdown. 
            # however, it also means that the server will exit when the main thread has no more to do, 
            # which may not be intuitive to the sdk user
            # thread.setDaemon(True)
            
            thread.start()
        except Exception as e:
            print(f"error setting up server on {host}:{port}", e)
            raise e

    def _find_free_port(self, host: str = "localhost", start_port=1500, end_port=1549):
        for port in range(start_port, end_port + 1):
            if self._is_port_available(host, port):
                # print(f"found free port {port} on {host}")
                return port
        raise RuntimeError(f"No free ports available in range {start_port}-{end_port}")

    def _get_or_create_agent(
        self, participant_id: str, run_id: str, username: str = None
    ) -> MinecraftAgent:
        agent = self._get_agent(participant_id, run_id)
        if agent:
            return agent

        if not self._agent_classes:
            raise ValueError("No agent classes registered")

        if username is None:
            username = next(iter(self._agent_classes))

        if username in self._agent_classes:
            agent_class = self._agent_classes[username]["class"]
        else:
            if "*" in self._agent_classes:
                agent_class = self._agent_classes["*"]["class"]
            else:
                raise ValueError(
                    f"No agent class registered for username: {username}, no catch-all agent found"
                )

        agent = agent_class(
            api_client=self._api_client, participant_id=participant_id, run_id=run_id
        )

        # this is in case we have used the '*' wildcard to register the agent
        # and we need to know the original username
        agent._original_username = username

        self._set_agent(participant_id, run_id, agent)

        return agent

    def _get_agent_key(self, participant_id: str, run_id: str) -> str:
        return f"{run_id}:{participant_id}"

    def _get_agent(self, participant_id: str, run_id: str) -> MinecraftAgent:
        agent_key = self._get_agent_key(participant_id, run_id)
        if agent_key in self._agents:
            return self._agents[agent_key]
        return None

    def _set_agent(self, participant_id: str, run_id: str, agent: MinecraftAgent):
        agent_key = self._get_agent_key(participant_id, run_id)
        self._agents[agent_key] = agent

    def _get_instance_counts(self, username=None):
        if username:
            if username not in self._agent_classes:
                return None
            class_name = self._agent_classes[username]["class"].__name__
            count = self._agent_classes[username]["count"]
            return {"class_name": class_name, "instances": count}

        counts = {}
        for username, info in self._agent_classes.items():
            counts[username] = {
                "class_name": info["class"].__name__,
                "instances": info["count"],
            }
        return counts

    def _create_flask_app(self):
        app = Flask(__name__)
        CORS(app)

        @app.after_request
        def after_request(response):
            self._logger.log_api_call(
                request.method, request.path, response.status_code
            )
            return response

        @app.route("/")
        def index():
            base_url = request.url_root.rstrip('/')
            response = {
                "status": "online",
                "agents": {},
            }

            for username in self._agent_classes.keys():
                agent_urls = {
                    "base": f"{base_url}/{username}",
                    "ping": f"{base_url}/{username}/ping",
                    "init": f"{base_url}/{username}/init",
                    "event": f"{base_url}/{username}/event",
                }
                response["agents"][username] = agent_urls

            return jsonify(response)

        @app.route("/<username>")
        def agent_index(username):
            if username not in self._agent_classes:
                return "", 404

            base_url = request.url_root.rstrip('/')
            stats = self._get_instance_counts(username)

            return jsonify(
                {
                    "status": "online",
                    "class_name": stats["class_name"],
                    "instances": stats["instances"],
                    "urls": {
                        "ping": f"{base_url}/{username}/ping",
                        "init": f"{base_url}/{username}/init",
                        "event": f"{base_url}/{username}/event",
                    },
                }
            )

        @app.route("/ping", defaults={"username": None})
        @app.route("/<username>/ping")
        def ping(username):
            if username:
                if username not in self._agent_classes:
                    return "", 404
                stats = self._get_instance_counts(username)
                return jsonify(
                    {
                        "status": "online",
                        "class_name": stats["class_name"],
                        "instances": stats["instances"],
                    }
                )

            return jsonify({"status": "online", "agents": self._get_instance_counts()})

        @app.route("/init", defaults={"username": None}, methods=["POST"])
        @app.route("/<username>/init", methods=["POST"])
        def init(username):
            data = request.get_json() or {}
            participant_id = data.get("participantId")
            run_id = data.get("runId")

            if participant_id is None:
                self._logger.log_error("Missing participantId in init request")
                return jsonify({"error": "participantId is required"}), 400

            try:
                agent = self._get_or_create_agent(
                    participant_id=participant_id,
                    run_id=run_id,
                    username=username,
                )

                # TODO: initialize memory here

                # run agent.init_participant()
                challenge_info = ChallengeInfo(
                    participant_id=participant_id,
                    run_id=data.get("runId"),
                    task=data.get("task"),
                    agent_modes=data.get("agent_modes"),
                    js_functions=data.get("js_functions"),
                    available_events=data.get("available_events"),
                )
                init_data = agent.init_participant(challenge_info)

                #TODO: check init_data is a valid InitParticipantResponse                
                
                self._logger.log_success(
                    f"Agent initialized for participant {participant_id}"
                )

                return jsonify(init_data)
            except ValueError as e:
                self._logger.log_error(f"Failed to initialize agent: {str(e)}")
                return jsonify({"error": str(e)}), 400

        @app.route("/event", defaults={"username": None}, methods=["POST"])
        @app.route("/<username>/event", methods=["POST"])
        def event(username):
            data = request.get_json() or {}
            observation = Observation.from_event(data)
            participant_id = data.get("participantId")
            run_id = data.get("runId")

            if participant_id is None:
                self._logger.log_error("Missing participantId in event request")
                return jsonify({"error": "participantId is required"}), 400

            try:
                agent = self._get_or_create_agent(
                    participant_id=participant_id, run_id=run_id, username=username
                )
                result = agent.on_event(observation)

                #TODO: check result is a valid OnEventResponse

                # run agent.on_event()
                return jsonify(result)
            except ValueError as e:
                self._logger.log_error(
                    f"Error in event handler for participant {participant_id}", e
                )
                return jsonify({"error": str(e)}), 400

        return app

    def _setup_signal_handlers(self):
        def handle_shutdown(signum, frame):
            self._logger.on_shutdown()
            self._shutdown_event.set()
            if self._server:
                self._server.shutdown()

        signal.signal(signal.SIGINT, handle_shutdown)
        signal.signal(signal.SIGTERM, handle_shutdown)

    def _get_tunnel_url(self, port):
        if hasattr(self, "_tunnel_url") and self._tunnel_url:
            return self._tunnel_url

        tunnel_instance, tunnel_url = create_tunnel(port)
        if tunnel_instance:
            self._logger.log_success(f"Public URL (tunnel) created successfully at {tunnel_url}")
            self._tunnel_url = tunnel_url
            return tunnel_url
        else:
            raise Exception("Failed to create a public URL (tunnel)")

    def _validate_api_key(self):
        """Validate the API key and print a helpful error message if it's not set."""
        try:
            self._api_client.validate_api_key()
        except Exception as e:
            # If it's still not set, then log an error and raise an exception
            self._logger.log_error(
                f"\n> API key required\n\n"
                f"Setup:\n"
                f"  1. Get your key: {KRADLE_URL}\n"
                f"  2. EITHER set the KRADLE_API_KEY environment variable as your key\n"
                f"     OR use `{self.__class__.__name__}.set_api_key(API_KEY)` to set it\n"
            )
            raise e

    @classmethod
    def set_api_key(cls, api_key):
        """
        Set the API key for the agent manager.

        This method does not need to be called if the KRADLE_API_KEY environment variable is set.
        """
        instance = cls()
        instance._api_client.set_api_key(api_key)

    @classmethod
    def create_cloud_agent(cls, agent_class) -> tuple[Flask]:
        instance = cls()
        instance._validate_api_key()

        # Get the agent username
        username = agent_class.username
        if username is None:
            raise ValueError("Agent class must have a username attribute")
        if username != "*":
            print(f"Warning: only {username} will be available on the cloud agent")

        # Register new agent class
        if username not in instance._agent_classes:
            instance._agent_classes[username] = {"class": agent_class, "count": 1}

        if not instance._app:
            # Set up new server
            instance._app = instance._create_flask_app()
        return instance._app

    @classmethod
    def serve(
        cls,
        agent_class,
        create_public_url=False,
        public_url=None,
        host="localhost",
        port=None,
        debug=False,
    ) -> tuple[Flask, str]:
        """Non-blocking server that automatically handles agent instance lifecycle."""
        """If the server is already running, it will be reused"""
        """The agent will be registered with Kradle with the given public_url or a new one will be created"""
        instance = cls()

        # Initialize or use existing server
        if not instance._app:
            # Set up new server
            instance._validate_api_key()
            instance._app = instance._create_flask_app()
            instance.port = port if port is not None else instance._find_free_port(host)

            # Set up instance.url
            if create_public_url:
                # Make a public URL if requested
                if public_url:
                    raise ValueError("cannot specify public_url if create_public_url is True")
                instance.url = f"{instance._get_tunnel_url(instance.port)}"
            else:
                if public_url:
                    instance.url = public_url
                    instance._logger.log_info(f"User specified public URL: {public_url}")
                else:
                    instance.url = f"http://{host}:{instance.port}"
                    instance._logger.log_info(f"Using local URL: http://{host}:{instance.port}")

            instance._setup_server(host, instance.port, debug)
        else:
            # Use existing server
            if not instance.url:
                raise ValueError("server not setup")
            if public_url and instance.url != public_url:
                instance._logger.log_warning(f"public_url does not match the server URL: {instance.url} != {public_url}")

        # Get the agent username
        username = agent_class.username
        agent_url = f"{instance.url}/{username}"

        if username not in instance._agent_classes:
            # Register the agent class with the agent manager
            instance._agent_classes[username] = {"class": agent_class, "count": 1}
        
            
            # Update the agent's URL on Kradle.
            try:
                # Let's first assume the agent already exists
                instance._api_client.agents.update(
                    username,
                    name=agent_class.display_name or agent_class.__name__,
                    url=agent_url,
                    description=agent_class.description
                    or "Created by the Kradle Python SDK",
                )
                instance._logger.display_agent_registered_banner({
                    "agent_username": username,
                    "agent_edit_url": f"{instance._kradle_url}/workbench/agents/{username}/edit",
                    "agent_url": agent_url,
                })
            except KradleAPIError as e:
                if e.status_code == 404:
                    # The agent doesn't already exist, so we'll create it
                    instance._logger.log_info(
                        f"Agent '{username}' not found, creating it"
                    )
                    instance._api_client.agents.create(
                        username,
                        name=agent_class.display_name or agent_class.__name__,
                        url=agent_url,
                        description=agent_class.description
                        or "Created by the Kradle Python SDK",
                    )
                    instance._logger.display_agent_registered_banner({
                        "agent_username": username,
                        "agent_edit_url": f"{instance._kradle_url}/workbench/agents/{username}/edit",
                        "agent_url": agent_url,
                    })
                else:
                    instance._logger.log_error(
                        f"Failed to create/update agent '{username}'", e
                    )
                    sys.exit(1)
            except Exception as e:
                instance._logger.log_error(
                    f"Failed to create/update agent '{username}'", e
                )
                sys.exit(1)

        return instance._app, agent_url
