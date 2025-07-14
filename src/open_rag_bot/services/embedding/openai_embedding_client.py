from openai import OpenAI
from tqdm import tqdm

from open_rag_bot.config.settings import openai_api_key
from open_rag_bot.exceptions import MissingProviderAPIKeyError
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(
        self, api_key: str = openai_api_key, model: str = "text-embedding-3-small"
    ):
        if not api_key:
            raise MissingProviderAPIKeyError("OpenAI")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def encode(
        self, texts: list[str], show_progress: bool = False
    ) -> list[list[float]]:
        output = []
        for text in tqdm(texts, desc="Embedding", disable=not show_progress):
            response = self.client.embeddings.create(input=text, model=self.model)
            output.append(response.data[0].embedding)
        return output
