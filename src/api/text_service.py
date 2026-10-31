from typing import List, Dict
from src.api.client import OpenRouterClient

class TextService:
    def __init__(self, client: OpenRouterClient):
        self.client = client

    def generate_document(self, topic: str, model: str = "perplexity/sonar-reasoning") -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": f"Write a comprehensive technical report on: {topic}. Include markdown citations."}]
        }
        res = self.client.post("chat/completions", payload)
        return res.json()['choices'][0]['message']['content']

    def selective_edit(self, block: str, action: str, model: str = "anthropic/claude-3.5-sonnet") -> str:
        prompt = f"Perform the following operation: '{action}' on this text block. Return ONLY the modified text:\n\n{block}"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        res = self.client.post("chat/completions", payload)
        return res.json()['choices'][0]['message']['content']

    def generate_plotly_code(self, context: str, query: str, model: str = "google/gemini-1.5-pro") -> str:
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
