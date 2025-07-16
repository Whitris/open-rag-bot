from groq import Groq
from tqdm import tqdm

from open_rag_bot.config.settings import get_settings
from open_rag_bot.exceptions import MissingProviderAPIKeyError
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient


settings = get_settings()


class GroqEmbeddingClient(EmbeddingClient):
    def __init__(
        self, api_key: str = settings.api.groq, model: str = "llama-3.3-70b-versatile"
    ):
        if not api_key:
            raise MissingProviderAPIKeyError("Groq")
        self.client = Groq(api_key=api_key)
        self.model = model

    def encode(
        self, texts: list[str], show_progress: bool = False
    ) -> list[list[float]]:
        output = []
        for text in tqdm(texts, desc="Embedding", disable=not show_progress):
            response = self.client.embeddings.create(input=text, model=self.model)
            output.append(response.data[0].embedding)
        return output
