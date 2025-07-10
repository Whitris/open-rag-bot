import chromadb
import numpy as np

from src.core.loader import load_index
from src.core.retriever import retrieve_relevant_docs


def test_load_index_returns_collection(tmp_path):
    collection = load_index(tmp_path, collection_name="test")
    assert collection.name == "test"


def test_retrieve_relevant_docs(tmp_path):
    client = chromadb.PersistentClient(path=str(tmp_path))
    collection = client.get_or_create_collection(name="test")
    docs = ["a", "b", "c"]
    embeddings = np.array([[1.0], [2.0], [3.0]])
    collection.add(
        documents=docs,
        ids=[str(i) for i in range(len(docs))],
        embeddings=embeddings.tolist(),
    )

    class DummyModel:
        def encode(self, texts):
            return np.array([[1.5]])

    model = DummyModel()
    results = retrieve_relevant_docs(
        "question",
        model,
        collection,
        # docs,
        k=2,
    )
    assert results
    assert all(res in docs for res in results)
