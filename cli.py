import typer

from src.core.chat_bot import get_chat_bot

app = typer.Typer(help="RAG Chatbot CLI")


@app.command()
def chat():
    history = [
        {
            "role": "system",
            "content": "You are a virtual assistant. Always answer in the question language.",
        }
    ]
    chat_bot = get_chat_bot(history)
    typer.echo("Chatbot started. Type your question ('exit' to exit).")

    while True:
        try:
            question = typer.prompt("You")
            if question.strip().lower() in {"exit", "quit"}:
                typer.echo("Goodbye.")
                break
            response = chat_bot.answer(question)
            typer.echo(f"Bot: {response}\n")
        except (KeyboardInterrupt, EOFError, typer.Abort):
            typer.echo("Interrupted. Goodbye.")
            break
        except Exception as e:
            typer.echo(f"Error: {e}")


if __name__ == "__main__":
    app()
