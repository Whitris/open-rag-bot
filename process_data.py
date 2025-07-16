import logging
from pathlib import Path
from time import perf_counter

import typer

from open_rag_bot.data.load import get_all_files, process_files
from open_rag_bot.data.save import save_chunks_to_csv

app = typer.Typer()


@app.command()
def process(
    input_dir: str = typer.Argument(..., help="Input docs directory"),
    output_csv_path: str = typer.Argument(..., help="Output CSV path"),
    chunk_size: int = typer.Option(500, help="Chunk size in characters"),
    max_files: int = typer.Option(-1, help="Max number of files to be processed"),
    formats: str = typer.Option(
        "pdf,txt,docx", help="Formati da processare, separati da virgola"
    ),
):
    """Extract text from documents (pdf, txt, docx) and save chunks to a CSV for RAG."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    input_path = Path(input_dir)
    if not input_path.is_dir():
        typer.echo(f"Errore: Cartella {input_dir} non trovata.", err=True)
        raise typer.Exit(1)

    output_csv_path = Path(output_csv_path)

    start = perf_counter()
    extensions = ["." + ext.strip().lower() for ext in formats.split(",")]
    file_paths = get_all_files(input_dir, extensions=extensions)
    if not file_paths:
        typer.echo("Nessun file trovato nei formati specificati.", err=True)
        raise typer.Exit(1)

    logging.info(f"Trovati {len(file_paths)} file da processare")
    chunks = process_files(file_paths, chunk_size=chunk_size, max_files=max_files)
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    save_chunks_to_csv(chunks, output_csv_path)
    logging.info(
        f"Completato: {len(file_paths)} file, {len(chunks)} chunk, {perf_counter() - start:.2f} s"
    )


if __name__ == "__main__":
    app()
