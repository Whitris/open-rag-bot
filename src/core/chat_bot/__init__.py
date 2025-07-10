from src.core.chat_bot.chat_bot import RagChatBot
from src.core.retriever import get_context_retriever
from src.services import get_embedding_client, get_llm_client


def get_chat_bot(history: list[dict]) -> RagChatBot:
    embedding_client = get_embedding_client()
    llm_client = get_llm_client()
    retriever = get_context_retriever()

    return RagChatBot(
        embedding_client=embedding_client,
        llm_client=llm_client,
        retriever=retriever,
        history=history,
    )
