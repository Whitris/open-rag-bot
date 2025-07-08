import os
import tempfile
import numpy as np
import pandas as pd
import pytest
import faiss

from src.data.embeddings import (
    load_texts,
    generate_embeddings,
    build_or_load_index,
    add_embeddings_to_index,
    save_index,
)


class DummyModel:
    def encode(self, texts):
        return np.ones((len(texts), 8))


def test_load_texts(tmp_path):
    csv_path = tmp_path / "texts.csv"
    df = pd.DataFrame({"text": ["a", "b", "c"]})
    df.to_csv(csv_path, index=False)
    texts = load_texts(str(csv_path))
    assert texts == ["a", "b", "c"]


def test_generate_embeddings():
    texts = ["test1", "test2"]
    model = DummyModel()
    embeddings = generate_embeddings(model, texts)
    assert embeddings.shape == (2, 8)
    assert np.allclose(embeddings, 1)


def test_build_or_load_index_creates_new():
    embeddings = np.ones((5, 16))
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "index.faiss")
        index = build_or_load_index(embeddings, index_path)
        assert isinstance(index, faiss.IndexFlatL2)
        assert index.d == 16


def test_build_or_load_index_loads_existing(tmp_path):
    dim = 10
    index = faiss.IndexFlatL2(dim)
    index_path = tmp_path / "idx.faiss"
    faiss.write_index(index, str(index_path))
    loaded = build_or_load_index(np.ones((2, dim)), str(index_path))
    assert isinstance(loaded, faiss.IndexFlatL2)
    assert loaded.d == dim


def test_add_and_save_index(tmp_path):
    embeddings = np.random.rand(3, 8)
    index = faiss.IndexFlatL2(8)
    add_embeddings_to_index(index, embeddings)
    assert index.ntotal == 3
    index_path = tmp_path / "save_test.faiss"
    save_index(index, str(index_path))
    assert os.path.isfile(index_path)


@pytest.mark.parametrize("n_texts, n_dim", [(2, 8), (10, 32)])
def test_end_to_end(tmp_path, n_texts, n_dim):
    texts = [f"text {i}" for i in range(n_texts)]
    df = pd.DataFrame({"text": texts})
    csv_path = tmp_path / "texts.csv"
    df.to_csv(csv_path, index=False)

    class Dummy:
        def encode(self, ts):
            return np.ones((len(ts), n_dim))

    model = Dummy()

    loaded_texts = load_texts(str(csv_path))
    assert loaded_texts == texts
    embeddings = generate_embeddings(model, loaded_texts)
    index_path = tmp_path / "e2e.faiss"
    index = build_or_load_index(embeddings, str(index_path))
    add_embeddings_to_index(index, embeddings)
    save_index(index, str(index_path))
    assert os.path.isfile(index_path)
