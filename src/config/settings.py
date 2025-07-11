import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("src/config/.env", override=True)

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


BASE_DIR = Path(__file__).resolve().parent.parent.parent
data_dir = BASE_DIR / "data"
input_dir = BASE_DIR / "input_docs"
processed_dir = data_dir / "processed"
index_dir = data_dir / "index"

input_dir = input_dir / "docs"
csv_path = processed_dir / "stuff.csv"
default_chroma_path = index_dir / "chromadb"
default_collection_name = "documents"

icon_path = os.getenv("ICON_PATH")
