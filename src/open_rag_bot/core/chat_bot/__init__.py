from open_rag_bot.core.chat_bot.chat_bot import RagChatBot
from open_rag_bot.core.retriever import get_context_retriever
from open_rag_bot.services import get_embedding_client, get_llm_client


def get_chat_bot(
    collection_dir: str, collection_name: str, history: list[dict]
) -> RagChatBot:
    embedding_client = get_embedding_client()
    llm_client = get_llm_client()
    retriever = get_context_retriever(
        collection_dir=collection_dir,
        collection_name=collection_name,
        embedding_client=embedding_client,
    )

    return RagChatBot(
        embedding_client=embedding_client,
        llm_client=llm_client,
        retriever=retriever,
        history=history,
    )
