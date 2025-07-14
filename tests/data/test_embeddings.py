import os

import numpy as np
import pandas as pd
import pytest

from open_rag_bot.data.embeddings import (
    add_embeddings_to_collection,
    build_or_load_collection,
    generate_embeddings,
    load_texts_with_metadata,
)
from open_rag_bot.exceptions import MissingCSVColumnError


class DummyModel:
    def encode(self, texts, show_progress=False):
        return np.ones((len(texts), 8)).tolist()


@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame(
        [
            {
                "chunk_id": i,
                "filename": f"file_{i}.txt",
                "title": f"title_{i}",
                "text": f"text_{i}",
            }
            for i in range(3)
        ]
    )
    csv_path = tmp_path / "sample.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path), df


def test_load_texts_with_metadata(sample_csv):
    csv_path, df = sample_csv
    entries = load_texts_with_metadata(csv_path)
    assert isinstance(entries, list)
    assert all(isinstance(e, dict) for e in entries)
    assert entries[0]["text"] == "text_0"
    assert entries[1]["filename"] == "file_1.txt"


def test_generate_embeddings():
    texts = ["foo", "bar", "baz"]
    model = DummyModel()
    embeddings = generate_embeddings(model, texts)
    assert isinstance(embeddings, list)
    assert np.array(embeddings).shape == (3, 8)
    assert all(np.allclose(e, 1) for e in embeddings)


def test_build_or_load_collection(tmp_path):
    chroma_dir = str(tmp_path / "chroma_db")
    collection_name = "test_collection"
    collection = build_or_load_collection(chroma_dir, collection_name)
    assert hasattr(collection, "add")
    # Test che la directory viene creata
    assert os.path.isdir(chroma_dir)


def test_add_embeddings_to_collection(tmp_path):
    chroma_dir = str(tmp_path / "chroma_db2")
    collection_name = "coll"
    collection = build_or_load_collection(chroma_dir, collection_name)
    # Dummy data
    texts = ["abc", "def"]
    embeddings = np.ones((2, 8))
    metadatas = [
        {"filename": "f1.txt", "title": "t1"},
        {"filename": "f2.txt", "title": "t2"},
    ]
    ids = ["1", "2"]
    add_embeddings_to_collection(collection, embeddings, texts, metadatas, ids)
    # Check retrieval
    res = collection.get(ids=["1", "2"])
    assert set(res["ids"]) == set(ids)
    assert res["metadatas"][0]["filename"] == "f1.txt"


@pytest.mark.parametrize(("n_texts", "n_dim"), [(2, 8), (10, 4)])
def test_end_to_end(tmp_path, n_texts, n_dim):
    df = pd.DataFrame(
        [
            {
                "chunk_id": i,
                "filename": f"f_{i}.txt",
                "title": f"title_{i}",
                "text": f"text_{i}",
            }
            for i in range(n_texts)
        ]
    )
    csv_path = tmp_path / "all.csv"
    df.to_csv(csv_path, index=False)

    class Dummy:
        def encode(self, ts, show_progress=False):
            return np.ones((len(ts), n_dim)).tolist()

    model = Dummy()

    entries = load_texts_with_metadata(str(csv_path))
    texts = [e["text"] for e in entries]
    metadatas = [
        {"filename": e["filename"], "title": e["title"], "chunk_id": str(e["chunk_id"])}
        for e in entries
    ]
    ids = [str(e["chunk_id"]) for e in entries]
    embeddings = generate_embeddings(model, texts)
    chroma_dir = str(tmp_path / "dbend2end")
    coll = build_or_load_collection(chroma_dir, "finalcoll")
    add_embeddings_to_collection(coll, embeddings, texts, metadatas, ids)
    # Query per id
    got = coll.get(ids=[ids[0]])
    assert got["metadatas"][0]["filename"] == metadatas[0]["filename"]
    assert got["documents"][0] == texts[0]


def test_load_texts_with_missing_columns(tmp_path):
    """Should raise MissingCSVColumnError if CSV lacks required columns."""
    df = pd.DataFrame([{"foo": 1, "bar": 2}])
    csv_path = tmp_path / "bad.csv"
    df.to_csv(csv_path, index=False)
    with pytest.raises(MissingCSVColumnError):
        load_texts_with_metadata(str(csv_path))
