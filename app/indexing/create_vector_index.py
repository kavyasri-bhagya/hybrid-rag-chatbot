from app.database.connection import get_connection


def create_index():

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Optional check: confirm pgvector extension exists
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        print("Vector Index Step Skipped Safely")
        print("Reason: pgvector does not support indexing")
        print("for 3072-dimensional embeddings in this setup.\n")

        print("Your system will still work using:")
        print("- Sequential vector search (pgvector)")
        print("- BM25 keyword search")
        print("- RRF fusion\n")

    except Exception as e:

        print("Error:", str(e))

    finally:

        cur.close()
        conn.close()


if __name__ == "__main__":
    create_index()