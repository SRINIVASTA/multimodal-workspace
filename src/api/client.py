import requests
from typing import Dict, Any
from src.config import settings

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.BASE_URL

    def post(self, endpoint: str, payload: Dict[str, Any]) -> requests.Response:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
        
        response = requests.post(
            url=f"{self.base_url}/{endpoint}",
            headers=settings.headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response
