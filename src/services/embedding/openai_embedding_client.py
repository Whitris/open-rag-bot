from openai import OpenAI
from tqdm import tqdm
from src.services.embedding.embedding_client import EmbeddingClient
from src.config.settings import openai_api_key


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(
        self, api_key: str = openai_api_key, model: str = "text-embedding-3-small"
    ):
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
