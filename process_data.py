import typer
import logging
from pathlib import Path
from time import perf_counter

from src.data.load import get_all_files, process_files
from src.data.save import save_chunks_to_csv

app = typer.Typer()


@app.command()
def process(
    input_dir: str = typer.Argument(..., help="Directory di input con i documenti"),
    output_csv: str = typer.Argument(..., help="Percorso file CSV di output"),
    chunk_size: int = typer.Option(500, help="Dimensione chunk in caratteri"),
    max_files: int = typer.Option(-1, help="Numero massimo di file da processare"),
    formats: str = typer.Option(
        "pdf,txt,docx", help="Formati da processare, separati da virgola"
    ),
):
    """
    Estrai testo da documenti (pdf, txt, docx) e salva i chunk in un CSV per RAG.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    input_path = Path(input_dir)
    if not input_path.is_dir():
        typer.echo(f"Errore: Cartella {input_dir} non trovata.", err=True)
        raise typer.Exit(1)

    start = perf_counter()
    extensions = ["." + ext.strip().lower() for ext in formats.split(",")]
    file_paths = get_all_files(input_dir, extensions=extensions)
    if not file_paths:
        typer.echo("Nessun file trovato nei formati specificati.", err=True)
        raise typer.Exit(1)

    logging.info(f"Trovati {len(file_paths)} file da processare")
    chunks = process_files(file_paths, chunk_size=chunk_size, max_files=max_files)
    save_chunks_to_csv(chunks, output_csv)
    logging.info(
        f"Completato: {len(file_paths)} file, {len(chunks)} chunk, {perf_counter() - start:.2f} s"
    )


if __name__ == "__main__":
    app()
