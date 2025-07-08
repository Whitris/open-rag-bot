import numpy as np


def retrieve_relevant_docs(question, model, index, stuff, k=5):
    embedding = model.encode([question])
    _, indices = index.search(np.array(embedding), k)
    return [stuff[i] for i in indices.flatten()]
