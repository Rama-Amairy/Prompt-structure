from abc import ABC, abstractmethod
from logs import log_info


class BaseModel(ABC):
    """Abstract base class for all AI models"""

    def __init__(self, model_name: str, api_key: str):
        """
        Initialize base model properties

        Args:
            model_name: Identifier for the AI model
            api_key: Authentication key if required
        """
        self.model_name = (model_name,)
        self.api_key = (api_key,)
        self.is_load = (False,)
        log_info(f"init base model class for: {self.model_name}")

    @abstractmethod
    def load_model(self):
        """Load the model (implementation specific)"""

    @abstractmethod
    def generate(self, prompt, **kwargs) -> str:
        """
        Generate response from prompt

        Args:
            prompt: Input text
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
