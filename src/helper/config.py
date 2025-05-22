import os
from functools import lru_cache
from pydantic_settings import BaseSettings


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


class Settings(BaseSettings):
    # app
    APP_NAME: str = "Defult name"
    APP_VERSION: str = "0"
    CHATBOT_NAME: str = "Nothing"

    # model name
    MODEL_NAME: str = "qwen/qwen3-0.6b-04-28:free"
    OPENROUTER_API_KEY: str = "None"

    class Config:
        env_file = os.path.join(root_dir, ".env")
        # env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.APP_VERSION)
    print(settings.CHATBOT_NAME)
