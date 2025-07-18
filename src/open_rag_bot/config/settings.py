from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from open_rag_bot.exceptions import MissingProviderAPIKeyError


load_dotenv(".env", override=True)


class ApiKeysSettings(BaseSettings):
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def openai(self) -> str:
        if not self.openai_api_key:
            raise MissingProviderAPIKeyError("openai")
        return self.openai_api_key


class AppSettings(BaseSettings):
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-large"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4.1-mini"
    small_llm_model: str = "gpt-4.1-nano"
    collection_dir: Path = Field(..., description="Directory for the Chroma index")
    collection_name: str = Field(..., description="Name for the Chroma collection")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
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
