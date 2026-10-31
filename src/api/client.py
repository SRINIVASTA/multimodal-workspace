import requests
from typing import Dict, Any
from src.config import settings

class OpenRouterClient:
    def __init__(self):
        self._raw_base_url = settings.BASE_URL

    def post(self, endpoint: str, payload: Dict[str, Any]) -> requests.Response:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
        
        # Strip trailing slashes safely
        base_clean = settings.BASE_URL.strip("/")
        
        # Detect if it's an image generation payload route
        if "images/generations" in endpoint:
            # Force target routing straight to the standard v1 images structure
            full_target_url = "https://openrouter.ai/api/v1/images/generations"
        else:
            if not base_clean.endswith("api/v1"):
                base_route = f"{base_clean}/api/v1"
            else:
                base_route = base_clean
            clean_endpoint = endpoint.lstrip("/")
            full_target_url = f"{base_route}/{clean_endpoint}"
        
        response = requests.post(
            url=full_target_url,
            headers=settings.headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response
