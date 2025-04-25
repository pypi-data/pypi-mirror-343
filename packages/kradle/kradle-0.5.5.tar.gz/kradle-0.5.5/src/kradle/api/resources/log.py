"""Run-specific API operations."""

from typing import Dict, List, TypedDict, NotRequired
from ..http import HTTPClient
import json


class LogAPI:
    """Log management API endpoints."""

    def __init__(self, http: HTTPClient):
        self.http = http

    def create(self, run_id, participant_id, message):
        if not isinstance(message, str):
            message = json.dumps(message)
        return self.http.post(
            f"runs/{run_id}/logs",
            {"message": message, "participantId": participant_id},
        )

    def dump(self, run_id: str, page_size: int = 20) -> List[Dict]:
        """
        Get all logs for a specific run, handling pagination automatically.
        
        Args:
            run_id: The ID of the run to get logs for
            page_size: Number of logs to return per page
            
        Returns:
            List of all log entries for the run
        """
        all_logs = []
        page_token = None
        
        while True:
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            
            response = self.http.get(f"runs/{run_id}/logs", params)
            
            if "logs" in response and response["logs"]:
                all_logs.extend(response["logs"])
            
            # Check if there are more pages
            page_token = response.get("nextPageToken")
            if not page_token:
                break
                
        all_logs.reverse() # reverse the order of the logs to start with the oldest log

        return all_logs
