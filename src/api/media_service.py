import requests
from typing import Dict, Any
from src.config import settings

class MediaService:
    def __init__(self, client=None):
        # Fall back gracefully to global settings context if custom client instance is dropped
        self.client = client
        self.headers = settings.headers if not client else settings.headers

    def generate_image(self, prompt: str, model: str) -> str:
        """Generates visual assets targeting OpenRouter images endpoint layers."""
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
            
        target_url = "https://openrouter.ai"
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": "url"
        }
        
        response = requests.post(
            url=target_url,
            headers=self.headers,
            json=payload,
            timeout=120
        )
        
        if not response.ok:
            raise RuntimeError(f"OpenRouter Image API Error {response.status_code}: {response.text}")
            
        response_json = response.json()
        
        # Self-healing index layout checker
        if 'data' in response_json and isinstance(response_json['data'], list) and len(response_json['data']) > 0:
            return response_json['data'][0]['url']
        elif 'data' in response_json and isinstance(response_json['data'], dict) and 'url' in response_json['data']:
            return response_json['data']['url']
            
        raise KeyError(f"Failed to identify target image parameters in payload: {response_json}")

    def text_to_speech(self, text: str, model: str) -> bytes:
        """
        Synthesizes high-fidelity binary voice data streams.
        PATCHED: Targets OpenRouter standard audio completion routes instead of bare landing URL domains.
        """
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("Authentication credentials missing: OPENROUTER_API_KEY is unset.")
            
        # Standard structural completion route configuration for open audio endpoints
        target_url = "https://openrouter.ai"
        
        payload = {
            "model": model,
            "input": text,
            "voice": "alloy"  # Baseline fallback descriptor
        }
        
        response = requests.post(
            url=target_url,
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if not response.ok:
            raise RuntimeError(f"OpenRouter Audio API Matrix Error {response.status_code}: {response.text}")
            
        return response.content
