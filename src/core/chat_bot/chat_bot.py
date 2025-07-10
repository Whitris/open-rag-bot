from src.core.prompt import build_prompt
from src.core.retriever.retriever import ContextRetriever
from src.services.embedding.embedding_client import EmbeddingClient
from src.services.llm.llm_client import LLMClient


class RagChatBot:
    def __init__(
        self,
        embedding_client: EmbeddingClient,
        llm_client: LLMClient,
        retriever: ContextRetriever,
        history: list[dict] = [],
    ):
        self.embedding_client = embedding_client
        self.llm_client = llm_client
        self.retriever = retriever
        self.history = history

    def answer(self, question: str):
        self._add_to_history("user", question)

        context = self.retriever.retrieve_context(question=question)
        prompt = build_prompt(question, context)

        self._add_to_history("system", prompt)

        response = self.llm_client.generate_response(self.history)

        self._add_to_history("assistant", response)

        return response

    def _add_to_history(self, role: str, text: str):
        self.history.append({"role": role, "content": text})
