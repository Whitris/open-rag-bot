import typer

from open_rag_bot.config.settings import collection_dir, collection_name, csv_path
from open_rag_bot.data.embeddings import (
    add_embeddings_to_collection,
    build_or_load_collection,
    generate_embeddings,
    load_texts_with_metadata,
)
from open_rag_bot.services import get_embedding_client

app = typer.Typer()


@app.command()
def generate(
    csv_path: str = typer.Argument(csv_path, help="Path to CSV file with text data"),
):
    """Generate and store embeddings to Chroma vector DB."""
    entries = load_texts_with_metadata(csv_path)
    texts = [e["text"] for e in entries]
    metadatas = [
        {"filename": e["filename"], "title": e["title"], "chunk_id": str(e["chunk_id"])}
        for e in entries
    ]
    ids = [str(e["chunk_id"]) for e in entries]

    typer.echo(f"Processing {len(texts)} texts.")

    client = get_embedding_client()
    embeddings = generate_embeddings(client, texts, show_progress=True)
    collection_dir.parent.mkdir(parents=True, exist_ok=True)
    collection = build_or_load_collection(collection_dir, collection_name)
    add_embeddings_to_collection(collection, embeddings, texts, metadatas, ids)
    typer.echo(
        f"Embeddings and metadata added to Chroma collection '{collection_name}' in {collection_dir}"
    )


if __name__ == "__main__":
    app()
