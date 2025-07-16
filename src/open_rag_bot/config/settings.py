from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from open_rag_bot.exceptions import MissingProviderAPIKeyError, UnknownProviderError


load_dotenv(".env", override=True)


class ApiKeysSettings(BaseSettings):
    groq_api_key: str | None = Field(default=None, description="Groq API key")
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def groq(self) -> str:
        if not self.groq_api_key:
            raise MissingProviderAPIKeyError("groq")
        return self.groq_api_key

    @property
    def openai(self) -> str:
        if not self.openai_api_key:
            raise MissingProviderAPIKeyError("openai")
        return self.openai_api_key


class AppSettings(BaseSettings):
    embedding_provider: str = "openai"
    llm_provider: str = "groq"
    light_llm_model: str | None = None
    llm_model: str | None = None
    collection_dir: Path = Field(..., description="Directory for the Chroma index")
    collection_name: str = Field(..., description="Name for the Chroma collection")
    icon_path: Path | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def embedding_provider_validated(self) -> str:
        p = self.embedding_provider.lower()
        if p not in ("openai", "groq"):
            raise UnknownProviderError("embedding", p)
        return p

    @property
    def llm_provider_validated(self) -> str:
        p = self.llm_provider.lower()
        if p not in ("openai", "groq"):
            raise UnknownProviderError("llm", p)
        return p

    @property
    def light_llm_model_effective(self) -> str:
        if self.light_llm_model:
            return self.light_llm_model
        return (
            "llama-3.1-8b-instant"
            if self.llm_provider_validated == "groq"
            else "gpt-4.1-nano"
        )

    @property
    def llm_model_effective(self) -> str:
        if self.llm_model:
            return self.llm_model
        return (
            "llama-3.3-70b-versatile"
            if self.llm_provider_validated == "groq"
            else "gpt-4.1-mini"
        )


class Settings:
    def __init__(self):
        self.api = ApiKeysSettings()
        self.app = AppSettings()


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
