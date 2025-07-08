import pandas as pd
from faiss import read_index


def load_index(path="faiss_index.idx"):
    return read_index(str(path))


def load_csv(path="stuff.csv"):
    return pd.read_csv(path).dropna().to_numpy().flatten()
