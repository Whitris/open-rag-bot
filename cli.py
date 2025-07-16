import logging

import typer

from open_rag_bot.config.settings import get_settings
from open_rag_bot.core.chat_bot import get_chat_bot
from open_rag_bot.core.logging_config import setup_logging

setup_logging(level=logging.INFO, log_to_file=True, file_path="open_rag_bot.log")
logger = logging.getLogger(__name__)

app = typer.Typer(help="RAG Chatbot CLI")

settings = get_settings()


@app.command()
def chat(
    collection_dir: str = typer.Option(
        settings.app.collection_dir, help="Input collection directory"
    ),
    collection_name: str = typer.Option(
        settings.app.collection_name, help="Input collection name"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose (DEBUG) logging"
    ),
):
    """Interactive chatbot session in the terminal."""
    if verbose:
        setup_logging(
            level=logging.DEBUG, log_to_file=True, file_path="open_rag_bot.log"
        )
        logger.debug("Verbose logging enabled.")

    history = [
        {
            "role": "system",
            "content": "You are a virtual assistant. Always answer in the question language.",
        }
    ]
    chat_bot = get_chat_bot(collection_dir, collection_name, history)
    typer.echo("Chatbot started. Type your question ('exit' to exit).")

    while True:
        try:
            question = typer.prompt("You")
            if question.strip().lower() in {"exit", "quit"}:
                typer.echo("Goodbye.")
                logger.info("User exited the chat.")
                break
            response = chat_bot.answer(question)
            typer.echo(f"Bot: {response}\n")
            logger.info("User: %s | Bot: %s", question, response)
        except (KeyboardInterrupt, EOFError, typer.Abort):
            typer.echo("Interrupted. Goodbye.")
            logger.info("Chat interrupted by user.")
            break
        except Exception:
            typer.echo("Error: an unexpected error occurred. Check log for details.")
            logger.exception("Unexpected error during chat loop")


if __name__ == "__main__":
    app()
