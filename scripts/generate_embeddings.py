import argparse
from config.settings import index_path
from core.model import model
from data.embeddings import (
    load_texts,
    generate_embeddings,
    build_or_load_index,
    add_embeddings_to_index,
    save_index,
)


def main(
    csv_path: str, index_path: str = index_path, start_idx: int = 0, end_idx: int = None
):
    texts = load_texts(csv_path)
    if end_idx is None or end_idx > len(texts):
        end_idx = len(texts)
    selected_texts = texts[start_idx:end_idx]
    print(f"Processing {len(selected_texts)} texts from index {start_idx} to {end_idx}")

    embeddings = generate_embeddings(model, selected_texts)
    index = build_or_load_index(embeddings, index_path)
    add_embeddings_to_index(index, embeddings)
    save_index(index, index_path)
    print(f"Embeddings added and index saved to {index_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and store embeddings to Faiss index."
    )
    parser.add_argument(
        "--csv_path",
        type=str,
        default="stuff.csv",
        help="Path to CSV file with text data",
    )
    parser.add_argument(
        "--index_path", type=str, default=index_path, help="Path to FAISS index"
    )
    parser.add_argument(
        "--start_idx", type=int, default=0, help="Start index for processing"
    )
    parser.add_argument(
        "--end_idx", type=int, default=None, help="End index for processing"
    )
    args = parser.parse_args()

    main(
        csv_path=args.csv_path,
        index_path=args.index_path,
        start_idx=args.start_idx,
        end_idx=args.end_idx,
    )
