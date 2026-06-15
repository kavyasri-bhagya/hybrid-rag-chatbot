from google import genai

from app.core.config import GEMINI_API_KEY
from app.database.connection import get_connection

client = genai.Client(
    api_key=GEMINI_API_KEY
)

EMBEDDING_MODEL = "gemini-embedding-001"


def get_query_embedding(query):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query
    )

    return response.embeddings[0].values


def dense_search(query, top_k=20):

    query_embedding = get_query_embedding(query)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            file_name,
            chunk_id,
            chunk_text,
            1 - (embedding <=> %s::vector) AS score
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (
            str(query_embedding),
            str(query_embedding),
            top_k
        )
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows