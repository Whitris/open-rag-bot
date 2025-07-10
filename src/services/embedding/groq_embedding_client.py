from groq import Groq
from tqdm import tqdm

from src.config.settings import groq_api_key
from src.services.embedding.embedding_client import EmbeddingClient


class GroqEmbeddingClient(EmbeddingClient):
    def __init__(
        self, api_key: str = groq_api_key, model: str = "llama-3.3-70b-versatile"
    ):
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
