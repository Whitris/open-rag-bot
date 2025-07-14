def save_chunks_to_csv(chunks: list[dict], output_csv: str = "stuff.csv"):
    import pandas as pd

    data = [
        {
            "chunk_id": i,
            "filename": chunk["filename"],
            "title": chunk.get("title", ""),
            "text": chunk["text"],
            "length": len(chunk["text"]),
        }
        for i, chunk in enumerate(chunks)
    ]
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, encoding="utf-8")
