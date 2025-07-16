"""Utilities for retrieving relevant documents from a Chroma collection."""

from __future__ import annotations

from chromadb.api.models import Collection

from open_rag_bot.services.embedding.embedding_client import EmbeddingClient


class ContextRetriever:
    def __init__(self, collection: Collection, embedding_client: EmbeddingClient):
        self.collection = collection
        self.embedding_client = embedding_client

    def retrieve_context(self, question: str, k: int = 5):
        docs = self.retrieve_relevant_docs(question, k)
        context = self._format_context(docs)

        return context

    def retrieve_relevant_docs(self, question: str, k: int = 5):
        """Return the most relevant documents for a question.

        Args:
            question: The user question.
            model: Model used to generate the embedding of the question.
            collection: Chroma collection containing the document embeddings.
            k: Number of documents to retrieve.

        Returns:
            A list of documents ranked by relevance.

        """
        embedding = self.embedding_client.encode([question])[0]
        result = self.collection.query(query_embeddings=[embedding], n_results=k)

        docs = result.get("documents", [[]])
        metas = result.get("metadatas", [[]])

        return [
            {"content": content, "metadata": metadata}
            for content, metadata in zip(docs[0], metas[0], strict=False)
        ]

    def _format_context(self, docs: list[dict]) -> str:
        """Format documents for use in the prompt context."""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = (
                doc["metadata"].get("title")
                or doc["metadata"].get("source")
                or f"Document {i}"
            )
            formatted.append(f"Source: {source}\n{doc['content']}")
        return "\n\n".join(formatted)
