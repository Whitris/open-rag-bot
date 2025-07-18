import pytest

from open_rag_bot.config.settings import Settings
from open_rag_bot.exceptions import UnknownProviderError
from open_rag_bot.services import get_embedding_client, get_llm_client
from open_rag_bot.services.embedding.openai_embedding_client import (
    OpenAIEmbeddingClient,
)
from open_rag_bot.services.llm.openai_client import OpenAIClient


@pytest.fixture
def settings_factory(monkeypatch):
    def _factory(env: dict = None):
        base_env = {
            "COLLECTION_DIR": "tests/test_data",
            "COLLECTION_NAME": "test_collection",
        }
        if env:
            base_env.update(env)
        for key, val in base_env.items():
            monkeypatch.setenv(key, val)
        return Settings()

    return _factory


def test_get_llm_client_openai(settings_factory):
    s = settings_factory(
        {
            "LLM_PROVIDER": "openai",
            "OPENAI_API_KEY": "FAKE",
        }
    )

    client = get_llm_client(settings=s)
    assert isinstance(client, OpenAIClient)


def test_get_llm_client_unknown(settings_factory):
    s = settings_factory(
        {
            "LLM_PROVIDER": "unknown",
        }
    )

    with pytest.raises(UnknownProviderError, match="Unknown llm provider:*"):
        get_llm_client(settings=s)


def test_get_embedding_client_openai(settings_factory):
    s = settings_factory(
        {
            "EMBEDDING_PROVIDER": "openai",
            "GROQ_API_KEY": "FAKE",
        }
    )

    client = get_embedding_client(settings=s)
    assert isinstance(client, OpenAIEmbeddingClient)


def test_get_embedding_client_unknown(settings_factory):
    s = settings_factory(
        {
            "EMBEDDING_PROVIDER": "unknown",
        }
    )

    with pytest.raises(UnknownProviderError, match="Unknown embedding provider:*"):
        get_embedding_client(settings=s)
