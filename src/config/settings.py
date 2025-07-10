import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("src/config/.env", override=True)

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()

if not groq_api_key and llm_provider == "groq":
    raise RuntimeError("GROQ_API_KEY not set in environment or .env")

if not openai_api_key and ("openai" in [embedding_provider, llm_provider]):
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
data_dir = BASE_DIR / "data"
input_dir = BASE_DIR / "input_docs"
processed_dir = data_dir / "processed"
index_dir = data_dir / "index"

input_dir = input_dir / "docs"
csv_path = processed_dir / "stuff.csv"
default_chroma_path = index_dir / "chromadb"
default_collection_name = "documents"
