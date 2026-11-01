import requests
import base64
from typing import Dict, Any
from src.config import settings

class TranscriptionService:
    def __init__(self):
        self.headers = settings.headers
        self.base_url = "https://openrouter.ai"

    def _execute_post(self, endpoint_route: str, payload: Dict[str, Any]) -> Any:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("🔒 Key Error: OPENROUTER_API_KEY is missing from configuration profiles.")
            
        full_url = f"{self.base_url}/{endpoint_route.lstrip('/')}"
        response = requests.post(url=full_url, headers=self.headers, json=payload, timeout=120)
        
        if not response.ok:
            raise RuntimeError(f"OpenRouter API Network Crash {response.status_code}: {response.text[:200]}")
        return response.json()

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", model: str = "openai/whisper-large-v3") -> str:
        """Transcribes audio using modern multi-modal payload structures over chat completions."""
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        mime_type = f"audio/{audio_format}"
        if audio_format == "mp3":
            mime_type = "audio/mpeg"

        # Modern unified multi-modal payload formatting
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Provide an exact, clean transcription of this audio without additional commentary."},
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": base64_audio,
                                "format": audio_format if audio_format != "mp3" else "mp3"
                            }
                        }
                    ]
                }
            ]
        }
        
        res_json = self._execute_post("chat/completions", payload)
        if "choices" in res_json and len(res_json["choices"]) > 0:
            return res_json["choices"][0]["message"]["content"].strip()
        elif "text" in res_json:
            return res_json["text"]
            
        raise KeyError(f"Unexpected response structure from OpenRouter: {res_json}")
