from google import genai

from app.core.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="Machine learning is amazing"
)

print(
    len(
        response.embeddings[0].values
    )
)