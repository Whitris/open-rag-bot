from src.config.settings import light_llm_model, llm_model
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
        history: list[dict] = None,
    ):
        self.embedding_client = embedding_client
        self.llm_client = llm_client
        self.retriever = retriever
        self.history = history if history is not None else []

    def answer(self, question: str):
        self._add_to_history("user", question)

        rewritten_question = self._rewrite_question(question)
        context = self.retriever.retrieve_context(question=rewritten_question)
        prompt = build_prompt(question, context)

        self._add_to_history("system", prompt)

        response = self.llm_client.generate_response(self.history, llm_model)

        self._add_to_history("assistant", response)

        return response

    def _add_to_history(self, role: str, text: str):
        self.history.append({"role": role, "content": text})

    def _rewrite_question(self, question: str) -> str:
        if len(self.history) <= 2:
            return question

        last_history = [h for h in self.history if h["role"] in {"user", "assistant"}][-4:]
        conversation = ""
        for h in last_history:
            role = "User" if h["role"] == "user" else "Assistant"
            conversation += f"{role}: {h['content']}\n"

        rewriting_prompt = f"""
            Rewrite the user's last question by making it complete and self-sufficient,
            using the following conversation history:

            {conversation}

            Rewritten question:
            """
        rewritten = self.llm_client.generate_response(
            [{"role": "system", "content": rewriting_prompt}], light_llm_model
        )

        return rewritten.strip()
