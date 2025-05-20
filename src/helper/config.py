import os
from functools import lru_cache
from pydantic_settings import BaseSettings


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


class Settings(BaseSettings):
    # app
    APP_NAME: str
    APP_VERSION: str
    CHATBOT_NAME: str

    class Config:
        env_file = os.path.join(root_dir, ".env")
        # env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
