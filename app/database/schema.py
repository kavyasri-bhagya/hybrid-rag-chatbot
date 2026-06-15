from app.database.connection import get_connection


def create_table():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE EXTENSION IF NOT EXISTS vector;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            file_name TEXT NOT NULL,
            chunk_id INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding VECTOR(3072)
        );
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("documents table created")


if __name__ == "__main__":
    create_table()