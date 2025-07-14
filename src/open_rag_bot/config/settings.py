import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()

default_light_llm_model = (
    "llama-3.1-8b-instant" if llm_provider == "groq" else "gpt-4.1-nano"
)
light_llm_model = os.getenv("LIGHT_LLM_MODEL", default_light_llm_model).lower()

default_llm_model = (
    "llama-3.3-70b-versatile" if llm_provider == "groq" else "gpt-4.1-mini"
)
llm_model = os.getenv("LLM_MODEL", default_llm_model).lower()

data_dir = Path(os.getenv("DATA_DIR", "data"))
processed_dir = data_dir / "processed"

csv_path = processed_dir / "stuff.csv"

collection_dir = Path(os.getenv("COLLECTION_DIR", "data"))
collection_name = os.getenv("COLLECTION_NAME", "default")

icon_path = Path(os.getenv("ICON_PATH"))
