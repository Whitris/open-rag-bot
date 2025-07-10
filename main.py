from src.config.settings import default_collection_name, index_dir
from src.core.loader import load_index
from src.core.prompt import build_prompt
from src.core.retriever import format_context, retrieve_relevant_docs
from src.services import get_embedding_client, get_llm_client


def answer(
    question: str,
    embedding_client,
    llm_client,
    index,
    history: list[dict],
    k: int = 5,
) -> str:
    history.append({"role": "user", "content": question})
    retrieved_docs = retrieve_relevant_docs(question, embedding_client, index, k)
    context = format_context(retrieved_docs)
    prompt = build_prompt(question, context)
    history.append({"role": "system", "content": prompt})

    response = llm_client.generate_response(history)
    history.append({"role": "assistant", "content": response})
    return response


def main():
    embedding_client = get_embedding_client()
    llm_client = get_llm_client()
    try:
        index = load_index(index_dir, default_collection_name)
    except Exception as e:
        print(f"Errore nel caricamento dei dati: {e}")
        return

    history = [
        {
            "role": "system",
            "content": "You are a virtual assistant. Always answer in the question language.",
        }
    ]
    try:
        question = input("Domanda: ")
        while question:
            response = answer(question, embedding_client, llm_client, index, history)
            print(response)
            question = input("Domanda: ")
    except KeyboardInterrupt:
        print("\nInterrotto.")
    except Exception as e:
        print(f"Errore durante l'interazione: {e}")


if __name__ == "__main__":
    main()
