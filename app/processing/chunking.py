from pathlib import Path
import json
from app.ingestion.pdf_loader import load_pdfs
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

OUTPUT_FILE = Path("data/chunks/chunks.json")


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks():

    documents = load_pdfs()

    all_chunks = []

    for doc in documents:

        file_name = doc["file_name"]

        text = doc["text"]

        chunks = split_text(text)

        for idx, chunk in enumerate(chunks):

            all_chunks.append(
                {
                    "file_name": file_name,
                    "chunk_id": idx,
                    "chunk_text": chunk
                }
            )

    return all_chunks


def save_chunks():

    chunks = create_chunks()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(chunks)} chunks")


if __name__ == "__main__":

    save_chunks()