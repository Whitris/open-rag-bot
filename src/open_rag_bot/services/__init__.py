from open_rag_bot.exceptions import UnknownProviderError
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient
from open_rag_bot.services.llm.llm_client import LLMClient


def get_llm_client() -> LLMClient:
    from open_rag_bot.config.settings import llm_provider

    if llm_provider == "groq":
        from open_rag_bot.config.settings import groq_api_key
        from open_rag_bot.services.llm.groq_client import GroqClient

        return GroqClient(api_key=groq_api_key)
    elif llm_provider == "openai":
        from open_rag_bot.config.settings import openai_api_key
        from open_rag_bot.services.llm.openai_client import OpenAIClient

        return OpenAIClient(api_key=openai_api_key)
    else:
        raise UnknownProviderError("LLM", llm_provider)


def get_embedding_client() -> EmbeddingClient:
    from open_rag_bot.config.settings import embedding_provider

    if embedding_provider == "groq":
        from open_rag_bot.services.embedding.groq_embedding_client import (
            GroqEmbeddingClient,
        )

        return GroqEmbeddingClient()
    elif embedding_provider == "openai":
        from open_rag_bot.services.embedding.openai_embedding_client import (
            OpenAIEmbeddingClient,
        )

        return OpenAIEmbeddingClient()

    else:
        raise UnknownProviderError("embedding", embedding_provider)
