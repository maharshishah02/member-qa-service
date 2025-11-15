from typing import List, Dict, Any
import httpx
from .config import MESSAGES_URL


class MessageClient:
    def __init__(self, base_url: str = MESSAGES_URL):
        self.base_url = base_url

    def fetch_messages(self) -> List[Dict[str, Any]]:
        resp = httpx.get(self.base_url, timeout=10, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()

        # Case 1: already a list
        if isinstance(data, list):
            return data

        # Case 2: wrapped list under common keys
        if isinstance(data, dict):
            for key in ("messages", "data", "items", "results"):
                val = data.get(key)
                if isinstance(val, list):
                    return val

        # If we reach here, we truly don't understand the shape
        raise ValueError(
            f"Unexpected /messages response format: expected list or "
            f"object with messages/data/items/results list, got: {type(data).__name__}"
        )
