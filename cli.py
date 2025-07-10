import typer

from src.core.chat_bot import get_chat_bot

app = typer.Typer(help="RAG Chatbot CLI")


@app.command()
def chat(question: str = typer.Argument(..., help="Domanda da porre al sistema")):
    history = [
        {
            "role": "system",
            "content": "You are a virtual assistant. Always answer in the question language.",
        }
    ]
    chat_bot = get_chat_bot(history)
    response = chat_bot.answer(question)

    typer.echo(response)


if __name__ == "__main__":
    app()
