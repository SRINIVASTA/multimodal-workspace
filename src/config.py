import os
import streamlit as st
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str = "https://openrouter.ai/api/v1"
    APP_URL: str = "http://localhost:8501"
    
    @property
    def OPENROUTER_API_KEY(self) -> str:
        """Dynamically pulls OpenRouter credentials from platform secrets or env."""
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
        return os.getenv("OPENROUTER_API_KEY", "")
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
            "HTTP-Referer": self.APP_URL,
            "X-Title": "Enterprise Multi-Modal Studio",
            "Content-Type": "application/json"
        }

settings = Settings()
