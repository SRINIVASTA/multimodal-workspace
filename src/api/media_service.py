import requests
from typing import Dict, Any, List
from src.config import settings

class UnifiedAIService:
    def __init__(self):
        self.headers = settings.headers
        self.base_url = "https://openrouter.ai/api/v1"

    def _execute_post(self, endpoint_route: str, payload: Dict[str, Any], stream_bytes: bool = False) -> Any:
        """Central network execution bridge to gracefully handle OpenRouter status codes."""
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("🔒 Key Error: OPENROUTER_API_KEY is completely missing from configuration profiles.")
            
        full_url = f"{self.base_url}/{endpoint_route.lstrip('/')}"
        
        response = requests.post(
            url=full_url,
            headers=self.headers,
            json=payload,
            timeout=120
        )
        
        # Guard rails: Capture non-200 returns instantly before parsing strings
        if not response.ok:
            raise RuntimeError(f"OpenRouter API Network Crash {response.status_code}: {response.text[:200]}")
            
        if stream_bytes:
            return response.content
            
        try:
            return response.json()
        except ValueError:
            raise RuntimeError(f"API endpoint returned an invalid non-JSON layout frame template target: {response.text[:200]}")

    # =========================================================================
    # TAB 1: DOCUMENT / CHAT ENGINE COMPLETIONS
    # =========================================================================
    def generate_text(self, messages: List[Dict[str, str]], model: str, max_tokens: int = 1200) -> str:
        """Handles deep context white-paper analysis and structured reports generation."""
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
        res_json = self._execute_post("chat/completions", payload)
        
        if 'choices' not in res_json or not res_json['choices']:
            raise KeyError(f"Unexpected JSON block array formatting inside text stream return layer: {res_json}")
        return res_json['choices'][0]['message']['content']

    # =========================================================================
    # TAB 2: TEXT-TO-IMAGE ENGINE
    # =========================================================================
    def generate_image(self, prompt: str, model: str) -> str:
        """Handles deep creative diffusion image asset generation loops."""
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": "url"
        }
        res_json = self._execute_post("images", payload)
        
        if 'data' in res_json:
            if isinstance(res_json['data'], list) and len(res_json['data']) > 0:
                return res_json['data'][0]['url']
            elif isinstance(res_json['data'], dict) and 'url' in res_json['data']:
                return res_json['data']['url']
                
        raise KeyError(f"Failed to isolate target image URL values inside the response matrix arrays: {res_json}")

    # =========================================================================
    # TAB 3: HYPER-REALISTIC VOICE SYNTHESIS
    # =========================================================================
    def text_to_speech(self, text: str, model: str, voice: str = "alloy") -> bytes:
        """Synthesizes voice track files targeting OpenRouter official speech api pipelines."""
        payload = {
            "model": model,
            "input": text,
            "response_format": "mp3"
        }
        
        # FIX: Explicitly pop the voice parameter from the dict if it's empty to prevent Zod validation failures
        if voice and voice.strip():
            payload["voice"] = voice
            
        return self._execute_post("audio/speech", payload, stream_bytes=True)
