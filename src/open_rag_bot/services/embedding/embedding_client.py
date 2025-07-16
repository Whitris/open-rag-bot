from abc import ABC, abstractmethod


class EmbeddingClient(ABC):
    @abstractmethod
    def encode(
        self, texts: list[str], show_progress: bool = False
    ) -> list[list[float]]:
        pass
