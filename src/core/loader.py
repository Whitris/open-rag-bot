"""Utility functions to load data and Chroma collections."""

from pathlib import Path

import chromadb
import pandas as pd
from chromadb.api.models import Collection


def load_index(
    path: str | Path = "chromadb", collection_name: str = "default"
) -> Collection:
    """Load or create a Chroma collection.

    Args:
        path: Directory where the Chroma database is stored.
        collection_name: Name of the collection to load.

    Returns:
        The requested Chroma collection.
    """

    client = chromadb.PersistentClient(path=str(path))
    return client.get_or_create_collection(name=collection_name)


def load_csv(path: str | Path = "stuff.csv") -> list[str]:
    """Load text chunks from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        A list of text chunks with any empty rows removed.
    """

    data = pd.read_csv(path).dropna()
    return data.to_numpy().flatten().tolist()
