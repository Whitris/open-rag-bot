from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate_response(self, history: list[dict], model: str = None) -> str:
        pass
