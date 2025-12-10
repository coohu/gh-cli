import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class Config:
    BASE_URL = "https://api.github.com"
    API_VERSION = "application/vnd.github.v3+json"
    
    @staticmethod
    def get_token() -> Optional[str]:
        return os.environ.get("GITHUB_TOKEN")
    
    @staticmethod
    def get_headers(token: str) -> dict:
        return {
            "Authorization": f"token {token}",
            "Accept": Config.API_VERSION
        }

