import requests
from src.config import settings

class MediaService:
    def __init__(self, client=None):
        self.client = client

    def generate_image(self, prompt: str, model: str) -> bytes:
        """
        Generates images by targeting OpenRouter's official /api/v1/images route.
        Returns raw image bytes directly from the API stream layer.
        """
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
            
        # CORRECT DEDICATED IMAGE GENERATION PATH
        target_url = "https://openrouter.ai/api/v1/images"
        
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        response = requests.post(
            url=target_url,
            headers=settings.headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        # OpenRouter's unified image endpoint drops raw image data bytes back
        return response.content

    def text_to_speech(self, text: str, model: str) -> bytes:
        """Synthesizes high-fidelity voice track data streams."""
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
