from src.services.embedding.embedding_client import EmbeddingClient
from src.services.llm.llm_client import LLMClient


def get_llm_client() -> LLMClient:
    from src.config.settings import llm_provider

    if llm_provider == "groq":
        from src.config.settings import groq_api_key
        from src.services.llm.groq_client import GroqClient

        return GroqClient(api_key=groq_api_key)
    elif llm_provider == "openai":
        from src.config.settings import openai_api_key
        from src.services.llm.openai_client import OpenAIClient

        return OpenAIClient(api_key=openai_api_key)
    else:
        raise ValueError(f"Unknown LLM provider: {llm_provider}")


def get_embedding_client() -> EmbeddingClient:
    from src.config.settings import embedding_provider

    if embedding_provider == "groq":
        from src.services.embedding.groq_embedding_client import GroqEmbeddingClient

        return GroqEmbeddingClient()
    elif embedding_provider == "openai":
        from src.services.embedding.openai_embedding_client import OpenAIEmbeddingClient

        return OpenAIEmbeddingClient()

    else:
        raise ValueError(f"Unknown embedding provider: {embedding_provider}")
