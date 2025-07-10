import typer

from src.config.settings import default_chroma_path, default_collection_name
from src.core.loader import load_index
from src.core.prompt import build_prompt
from src.core.retriever import retrieve_relevant_docs
from src.services import get_embedding_client, get_llm_client

app = typer.Typer(help="RAG Chatbot CLI")


@app.command()
def chat(
    question: str = typer.Argument(..., help="Domanda da porre al sistema"),
    k: int = typer.Option(
        5, "--top-k", "-k", help="Numero di documenti rilevanti da considerare"
    ),
    language: str = typer.Option("italiano", help="Lingua della risposta"),
):
    """
    Chatta con il sistema su documenti già indicizzati.
    """
    embedding_client = get_embedding_client()
    llm_client = get_llm_client()
    index = load_index(default_chroma_path, default_collection_name)

    history = [
        {
            "role": "system",
            "content": f"Sei un assistente virtuale. Rispondi sempre in {language}.",
        }
    ]

    history.append({"role": "user", "content": question})
    retrieved_docs = retrieve_relevant_docs(question, embedding_client, index, k)
    context = " ".join(retrieved_docs)
    prompt = build_prompt(question, context)
    history.append({"role": "system", "content": prompt})

    response = llm_client.generate_response(history)
    history.append({"role": "assistant", "content": response})

    typer.echo(response)


if __name__ == "__main__":
    app()
