import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    BASE_URL: str = "https://openrouter.ai"
    APP_URL: str = "http://localhost:8501"
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
            "HTTP-Referer": self.APP_URL,
            "Content-Type": "application/json"
        }

settings = Settings()
