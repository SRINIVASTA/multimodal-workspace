from typing import List, Dict
from src.api.client import OpenRouterClient

class TextService:
    def __init__(self, client: OpenRouterClient):
        self.client = client

    def generate_document(self, topic: str, model: str = "google/gemini-2.5-flash") -> str:
        """Generates structured report matrices using an active, stable model identifier mapping."""
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user", 
                    "content": f"Write a comprehensive technical report on: {topic}. Include clean markdown citations."
                }
            ]
        }
        try:
            res = self.client.post("chat/completions", payload)
            response_json = res.json()
            
            if 'choices' not in response_json or not response_json['choices']:
                raise KeyError(f"Unexpected response structure or empty choices context: {response_json}")
                
            return response_json['choices'][0]['message']['content']
        except Exception as api_err:
            if hasattr(api_err, 'response') and api_err.response is not None:
                raise RuntimeError(f"OpenRouter Connection Error {api_err.response.status_code}: {api_err.response.text}")
            raise api_err

    def selective_edit(self, block: str, action: str, model: str = "google/gemini-2.5-flash") -> str:
        """Transforms distinct localized paragraphs with explicit array resolution bounds."""
        prompt = f"Perform the following operation: '{action}' on this text block. Return ONLY the modified text:\n\n{block}"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            res = self.client.post("chat/completions", payload)
            return res.json()['choices'][0]['message']['content']
        except Exception as api_err:
            if hasattr(api_err, 'response') and api_err.response is not None:
                raise RuntimeError(f"Selective Edit API Exception {api_err.response.status_code}: {api_err.response.text}")
            raise api_err

    def generate_plotly_code(self, context: str, query: str, model: str = "google/gemini-2.5-flash") -> str:
        """Generates executable Plotly graphs dynamically via programmatic execution parameters."""
        system_rules = "Write ONLY clean, executable Python code utilizing plotly.express. Output the chart object into a variable named 'fig'. Do not include markdown ticks."
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_rules},
                {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
            ]
        }
        res = self.client.post("chat/completions", payload)
        return res.json()['choices'][0]['message']['content']
