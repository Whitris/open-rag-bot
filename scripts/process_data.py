from pathlib import Path
from time import perf_counter

from data.data_processing import get_all_pdf_files, process_pdfs, save_chunks_to_csv
from src.config.settings import csv_path, input_dir


def main():
    chunk_size = 500
    max_files = -1

    if not Path(input_dir).is_dir():
        raise FileNotFoundError(f"Cartella {input_dir} non trovata.")

    start_time = perf_counter()

    pdf_paths = get_all_pdf_files(input_dir)
    chunks = process_pdfs(pdf_paths, chunk_size=chunk_size, max_files=max_files)
    save_chunks_to_csv(chunks, csv_path)

    print(f"Completato in {perf_counter() - start_time:.2f} secondi")


if __name__ == "__main__":
    main()
