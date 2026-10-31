import requests
from src.config import settings

class MediaService:
    def __init__(self, client=None):
        self.client = client

    def generate_image(self, prompt: str, model: str) -> str:
        """
        Generates images by targeting OpenRouter's official /api/v1/images route.
        Parses and returns the absolute hosted image asset URL string safely.
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
            
        # PRODUCTION FIX: Correctly targeting index 0 of the data array wrapper
        response_json = response.json()
        
        if 'data' in response_json and len(response_json['data']) > 0:
            return response_json['data'][0]['url']
        raise KeyError(f"Unexpected JSON structure returned from OpenRouter: {response_json}")

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
