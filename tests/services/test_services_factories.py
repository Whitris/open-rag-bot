import pytest

from open_rag_bot.config import settings as settings_module


@pytest.fixture(autouse=True)
def reset_settings():
    settings_module._settings = None
    yield
    settings_module._settings = None


def test_get_llm_client_groq(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "FAKE")
    from open_rag_bot.services import get_llm_client
    from open_rag_bot.services.llm.groq_client import GroqClient

    client = get_llm_client()
    assert isinstance(client, GroqClient)


def test_get_llm_client_openai(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "FAKE")
    from open_rag_bot.services import get_llm_client
    from open_rag_bot.services.llm.openai_client import OpenAIClient

    client = get_llm_client()
    assert isinstance(client, OpenAIClient)


def test_get_llm_client_unknown(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "sconosciuto")
    from open_rag_bot.exceptions import UnknownProviderError
    from open_rag_bot.services import get_llm_client
    import pytest

    with pytest.raises(UnknownProviderError, match="Unknown llm provider:*"):
        get_llm_client()


def test_get_embedding_client_groq(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "groq")
    from open_rag_bot.services import get_embedding_client
    from open_rag_bot.services.embedding.groq_embedding_client import (
        GroqEmbeddingClient,
    )

    client = get_embedding_client()
    assert isinstance(client, GroqEmbeddingClient)


def test_get_embedding_client_openai(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "openai")
    from open_rag_bot.services import get_embedding_client
    from open_rag_bot.services.embedding.openai_embedding_client import (
        OpenAIEmbeddingClient,
    )

    client = get_embedding_client()
    assert isinstance(client, OpenAIEmbeddingClient)


def test_get_embedding_client_unknown(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "invalid")
    from open_rag_bot.services import get_embedding_client
    from open_rag_bot.exceptions import UnknownProviderError
    import pytest

    with pytest.raises(UnknownProviderError, match="Unknown embedding provider:*"):
        get_embedding_client()
