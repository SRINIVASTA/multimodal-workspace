from typing import Dict
from src.api.client import OpenRouterClient

class MediaService:
    def __init__(self, client: OpenRouterClient):
        self.client = client

    def generate_image(self, prompt: str, model: str) -> str:
        """Generates creative assets using standard index zero layout array lookups."""
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": "url"
        }
        res = self.client.post("images/generations", payload)
        
        # PRODUCTION FIX: Added explicit index mapping [0] matching OpenRouter payload signatures
        return res.json()['data'][0]['url']

    def text_to_speech(self, text: str, model: str) -> bytes:
        payload = {
            "model": model,
            "input": text
        }
        res = self.client.post("audio/speech", payload)
        return res.content
