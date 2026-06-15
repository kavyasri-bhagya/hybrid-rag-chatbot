import json
from pathlib import Path

from app.database.connection import get_connection


EMBEDDINGS_FILE = Path(
    "data/outputs/embeddings.json"
)


def insert_embeddings():

    with open(
        EMBEDDINGS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        records = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    total = len(records)

    for index, record in enumerate(records, start=1):

        embedding = str(
            record["embedding"]
        )

        cur.execute(
            """
            INSERT INTO documents
            (
                file_name,
                chunk_id,
                chunk_text,
                embedding
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                record["file_name"],
                record["chunk_id"],
                record["chunk_text"],
                embedding
            )
        )

        if index % 25 == 0:
            conn.commit()

        print(
            f"[{index}/{total}] inserted"
        )

    conn.commit()

    cur.close()
    conn.close()

    print(
        f"\nInserted {total} rows"
    )


if __name__ == "__main__":
    insert_embeddings()