from open_rag_bot.config.settings import get_settings, Settings
from open_rag_bot.exceptions import UnknownProviderError
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient
from open_rag_bot.services.llm.llm_client import LLMClient


def get_llm_client(settings: Settings = None) -> LLMClient:
    settings = settings or get_settings()

    if settings.app.llm_provider == "openai":
        from open_rag_bot.services.llm.openai_client import OpenAIClient

        return OpenAIClient(api_key=settings.api.openai)
    else:
        raise UnknownProviderError("llm", settings.app.llm_provider)


def get_embedding_client(settings: Settings = None) -> EmbeddingClient:
    settings = settings or get_settings()

    if settings.app.embedding_provider == "openai":
        from open_rag_bot.services.embedding.openai_embedding_client import (
            OpenAIEmbeddingClient,
        )

        return OpenAIEmbeddingClient()
    else:
        raise UnknownProviderError("embedding", settings.app.embedding_provider)
