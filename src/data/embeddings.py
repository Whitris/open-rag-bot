import os
import numpy as np
import pandas as pd
import faiss


def load_texts(csv_path: str) -> list[str]:
    data = pd.read_csv(csv_path).dropna()
    return data.to_numpy().flatten().tolist()


def generate_embeddings(model, texts: list[str]) -> np.ndarray:
    return model.encode(texts)


def build_or_load_index(embeddings: np.ndarray, index_path: str) -> faiss.Index:
    if os.path.isfile(index_path):
        index = faiss.read_index(index_path)
    else:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
    return index


def add_embeddings_to_index(index: faiss.Index, embeddings: np.ndarray):
    index.add(embeddings.astype("float32"))


def save_index(index: faiss.Index, index_path: str):
    faiss.write_index(index, index_path)
