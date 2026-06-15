import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi

from app.database.connection import get_connection

INDEX_FILE = Path("data/bm25/bm25.pkl")


def build_bm25_index():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            file_name,
            chunk_id,
            chunk_text
        FROM documents
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    corpus = []
    metadata = []

    for row in rows:

        corpus.append(
            row[3].lower().split()
        )

        metadata.append(
            {
                "id": row[0],
                "file_name": row[1],
                "chunk_id": row[2],
                "chunk_text": row[3]
            }
        )

    bm25 = BM25Okapi(corpus)

    INDEX_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(INDEX_FILE, "wb") as f:

        pickle.dump(
            {
                "bm25": bm25,
                "metadata": metadata
            },
            f
        )

    print("BM25 index created")


if __name__ == "__main__":
    build_bm25_index()