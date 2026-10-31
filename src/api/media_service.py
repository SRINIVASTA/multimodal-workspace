import requests
from src.config import settings

class MediaService:
    def __init__(self, client=None):
        self.client = client

    def generate_image(self, prompt: str, model: str) -> str:
        """
        Generates images by targeting OpenRouter's official /api/v1/images route.
        Implements self-healing schema key detection for varying provider layouts.
        """
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
            
        target_url = "https://openrouter.ai/api/v1/images"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": "url"
        }
        
        response = requests.post(
            url=target_url,
            headers=settings.headers,
            json=payload,
            timeout=120
        )
        
        if not response.ok:
            raise RuntimeError(f"OpenRouter Image API Error {response.status_code}: {response.text}")
            
        response_json = response.json()
        
        # SELF-HEALING PAYLOAD CHECKER
        # Method 1: Check standard data list array structure
        if 'data' in response_json and isinstance(response_json['data'], list) and len(response_json['data']) > 0:
            return response_json['data'][0]['url']
        # Method 2: Check object map format directly
        elif 'data' in response_json and isinstance(response_json['data'], dict) and 'url' in response_json['data']:
            return response_json['data']['url']
            
        raise KeyError(f"Failed to identify target image link parameter fields in payload: {response_json}")

    def text_to_speech(self, text: str, model: str) -> bytes:
        """Synthesizes high-fidelity voice track data streams from the clean speech node."""
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
            
        target_url = "https://openrouter.ai"
        
        payload = {
            "model": model,
            "input": text
        }
        
        response = requests.post(
            url=target_url,
            headers=settings.headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.content
