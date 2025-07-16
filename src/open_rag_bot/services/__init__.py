from open_rag_bot.config.settings import get_settings, Settings
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient
from open_rag_bot.services.llm.llm_client import LLMClient


def get_llm_client(settings: Settings = None) -> LLMClient:
    settings = settings or get_settings()

    if settings.app.llm_provider_validated == "groq":
        from open_rag_bot.services.llm.groq_client import GroqClient

        return GroqClient(api_key=settings.api.groq)
    elif settings.app.llm_provider_validated == "openai":
        from open_rag_bot.services.llm.openai_client import OpenAIClient

        return OpenAIClient(api_key=settings.api.openai)
    else:
        raise ValueError(
            f"Unknown LLM provider: {settings.app.llm_provider_validated!r}"
        )


def get_embedding_client(settings: Settings = None) -> EmbeddingClient:
    settings = settings or get_settings()

    if settings.app.embedding_provider_validated == "groq":
        from open_rag_bot.services.embedding.groq_embedding_client import (
            GroqEmbeddingClient,
        )

        return GroqEmbeddingClient()
    elif settings.app.embedding_provider_validated == "openai":
        from open_rag_bot.services.embedding.openai_embedding_client import (
            OpenAIEmbeddingClient,
        )

        return OpenAIEmbeddingClient()
    else:
        raise ValueError(
            f"Unknown embedding provider: {settings.app.embedding_provider_validated!r}"
        )
