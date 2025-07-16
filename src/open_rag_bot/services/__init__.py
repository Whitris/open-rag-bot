from open_rag_bot.config.settings import get_settings
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient
from open_rag_bot.services.llm.llm_client import LLMClient


settings = get_settings()


def get_llm_client() -> LLMClient:
    if settings.app.llm_provider_validated == "groq":
        from open_rag_bot.services.llm.groq_client import GroqClient

        return GroqClient(api_key=settings.api.groq)
    elif settings.app.llm_provider_validated == "openai":
        from open_rag_bot.services.llm.openai_client import OpenAIClient

        return OpenAIClient(api_key=settings.api.openai)


def get_embedding_client() -> EmbeddingClient:
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
