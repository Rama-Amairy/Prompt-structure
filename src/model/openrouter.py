import os
import sys
import requests


try:
    MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.append(MAIN_DIR)
    from model import BaseModel
    from logs import log_info
except ImportError as ie:
    raise ImportError(f"ImportError in HuggingFace wrapper: {ie}") from ie


class OpenRouterModel(BaseModel):
    "implemntation of an openrouter model"

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name, api_key)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://127.0.0.1:8000",  # Required by OpenRouter
            "X-Title": "Advance Prompt",  # Required by OpenRouter
            "Content-Type": "application/json",
        }

    def load_model(self):
        """Verify API connectivity"""

        try:
            test_response = requests.get(
                f"{self.BASE_URL}/models", headers=self.headers, timeout=10
            )
            test_response.raise_for_status()
            self.is_load = True
            log_info(f"OpenRouter model '{self.model_name}' ready")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to OpenRouter: {e}") from e

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using Qwen 0.6B free model

        Args:
            prompt: Input text prompt
            **kwargs: Generation parameters:
                - max_tokens (int): Default 200
                - temperature (float): Default 0.7

        Returns:
            Generated text response
        """
        if not self.is_load:
            self.load_model()

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 200),
            "temperature": kwargs.get("temperature", 0.7),
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            raise RuntimeError(f"Generation failed: {e}") from e


# Example usage
if __name__ == "__main__":
    model = OpenRouterModel(
        model_name="qwen/qwen3-0.6b-04-28:free",
        api_key="Your-api-key",
    )

    try:
        response = model.generate("hi how are you?", temperature=0.5, max_tokens=150)
        print("Qwen 0.6B Response:")
        print(response)

    except Exception as e:
        print(f"Error: {e}")
