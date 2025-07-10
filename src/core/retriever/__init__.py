from src.config.settings import default_collection_name, index_dir
from src.core.loader import load_collection
from src.core.retriever.retriever import ContextRetriever
from src.services import get_embedding_client


def get_context_retriever() -> ContextRetriever:
    try:
        collection = load_collection(index_dir, default_collection_name)
    except Exception as e:
        raise Exception(f"Error while loading the collection: {e}")

    client = get_embedding_client()

    return ContextRetriever(collection=collection, embedding_client=client)
