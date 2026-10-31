import os
import streamlit as st
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str = "https://openrouter.ai"
    APP_URL: str = "http://localhost:8501"
    
    @property
    def OPENROUTER_API_KEY(self) -> str:
        """
        Dynamically fetches the OpenRouter API Key.
        Prioritizes Streamlit Secrets for cloud/production orchestration,
        falling back to local environment variables for system tooling/testing.
        """
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
        return os.getenv("OPENROUTER_API_KEY", "")
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
            "HTTP-Referer": self.APP_URL,
            "Content-Type": "application/json"
        }

settings = Settings()
