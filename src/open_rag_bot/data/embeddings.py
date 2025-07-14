from typing import Any

import chromadb
import pandas as pd

from open_rag_bot.exceptions import MissingCSVColumnError
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient


def load_texts_with_metadata(csv_path: str) -> list[dict[str, Any]]:
    """Load records from a CSV and return as a list of dicts with metadata.

    Args:
        csv_path (str): Path to CSV.

    Returns:
        List[Dict[str, Any]]: Records loaded from CSV.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    df = pd.read_csv(csv_path)
    required_cols = {"chunk_id", "filename", "title", "text"}
    missing = required_cols - set(df.columns)
    if missing:
        raise MissingCSVColumnError(missing)
    return df.to_dict(orient="records")


def generate_embeddings(
    client: EmbeddingClient, texts: list[str], show_progress: bool = False
):
    return client.encode(texts, show_progress)


def build_or_load_collection(chroma_dir, collection_name):
    client = chromadb.PersistentClient(path=chroma_dir)
    collection = client.get_or_create_collection(collection_name)
    return collection


def add_embeddings_to_collection(collection, embeddings, texts, metadatas, ids):
    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()
    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )
