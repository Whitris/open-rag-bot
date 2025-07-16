from open_rag_bot.core.loader import load_or_create_collection
from open_rag_bot.core.retriever.retriever import ContextRetriever
from open_rag_bot.exceptions import CollectionError
from open_rag_bot.services import get_embedding_client
from open_rag_bot.services.embedding.embedding_client import EmbeddingClient


def get_context_retriever(
    collection_dir: str,
    collection_name: str,
    embedding_client: EmbeddingClient | None = None,
) -> ContextRetriever:
    try:
        collection = load_or_create_collection(collection_dir, collection_name)
    except Exception as e:
        raise CollectionError from e

    embedding_client = embedding_client or get_embedding_client()
    return ContextRetriever(collection=collection, embedding_client=embedding_client)
