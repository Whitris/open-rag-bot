import pytest

from open_rag_bot.exceptions import UnknownProviderError
from open_rag_bot.services import get_embedding_client, get_llm_client


def test_get_llm_client_groq(mocker):
    mocker.patch("open_rag_bot.config.settings.llm_provider", "groq")
    mocker.patch("open_rag_bot.config.settings.groq_api_key", "FAKE")
    from open_rag_bot.services.llm.groq_client import GroqClient

    client = get_llm_client()
    assert isinstance(client, GroqClient)


def test_get_llm_client_openai(mocker):
    mocker.patch("open_rag_bot.config.settings.llm_provider", "openai")
    mocker.patch("open_rag_bot.config.settings.openai_api_key", "FAKE")
    from open_rag_bot.services.llm.openai_client import OpenAIClient

    client = get_llm_client()
    assert isinstance(client, OpenAIClient)


def test_get_llm_client_unknown(mocker):
    mocker.patch("open_rag_bot.config.settings.llm_provider", "sconosciuto")
    with pytest.raises(UnknownProviderError, match="Unknown LLM provider:*") as exc:
        get_llm_client()
    assert "Unknown LLM provider" in str(exc.value)


def test_get_embedding_client_groq(mocker):
    mocker.patch("open_rag_bot.config.settings.embedding_provider", "groq")
    from open_rag_bot.services.embedding.groq_embedding_client import (
        GroqEmbeddingClient,
    )

    client = get_embedding_client()
    assert isinstance(client, GroqEmbeddingClient)


def test_get_embedding_client_openai(mocker):
    mocker.patch("open_rag_bot.config.settings.embedding_provider", "openai")
    from open_rag_bot.services.embedding.openai_embedding_client import (
        OpenAIEmbeddingClient,
    )

    client = get_embedding_client()
    assert isinstance(client, OpenAIEmbeddingClient)


def test_get_embedding_client_unknown(mocker):
    mocker.patch("open_rag_bot.config.settings.embedding_provider", "invalid")
    with pytest.raises(
        UnknownProviderError, match="Unknown embedding provider:*"
    ) as exc:
        get_embedding_client()
    assert "Unknown embedding provider" in str(exc.value)
