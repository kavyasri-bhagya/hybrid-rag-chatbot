import json
import time
from pathlib import Path

from google import genai

from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

CHUNKS_FILE = Path("data/chunks/chunks.json")
OUTPUT_FILE = Path("data/outputs/embeddings.json")

EMBEDDING_MODEL = "gemini-embedding-001"


def get_embedding(text: str):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def generate_embeddings():

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embedded_chunks = []

    total = len(chunks)

    for index, chunk in enumerate(chunks, start=1):

        success = False

        while not success:

            try:

                embedding = get_embedding(
                    chunk["chunk_text"]
                )

                embedded_chunks.append(
                    {
                        "file_name": chunk["file_name"],
                        "chunk_id": chunk["chunk_id"],
                        "chunk_text": chunk["chunk_text"],
                        "embedding": embedding
                    }
                )

                print(
                    f"[{index}/{total}] "
                    f"{chunk['file_name']} "
                    f"Chunk {chunk['chunk_id']}"
                )

                success = True

                time.sleep(1)

            except Exception as e:

                error_text = str(e)

                if "429" in error_text:

                    print(
                        "\nRate limit reached."
                    )

                    print(
                        "Waiting 65 seconds..."
                    )

                    time.sleep(65)

                else:

                    raise e

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
            embedded_chunks,
            f
        )

    print(
        f"\nSaved {len(embedded_chunks)} embeddings"
    )


if __name__ == "__main__":
    generate_embeddings()