from google import genai

from app.core.config import GEMINI_API_KEY
from app.retrieval.hybrid_search import hybrid_search


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(question: str):

    results = hybrid_search(question)

    if not results:
        return "No relevant information found in the documents."
    context = ""

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)

    for i, row in enumerate(results, start=1):

        file_name = row[1]
        chunk_id = row[2]
        chunk_text = row[3]

        print(f"\n[{i}] File     : {file_name}")
        print(f"    Chunk ID : {chunk_id}")

        context += f"""
SOURCE [{i}]
File: {file_name}
Chunk ID: {chunk_id}

Text:
{chunk_text}

"""

    print("\n" + "=" * 80)
    prompt = f"""
You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

Rules:
1. Do not use external knowledge.
2. If the answer is not present in the context, respond exactly:
   "I could not find the answer in the documents."
3. Be concise and accurate.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    print("=" * 80)
    print("Type 'exit' to quit")
    print("=" * 80)

    while True:

        question = input("\nAsk: ").strip()

        if question.lower() == "exit":
            break

        try:

            answer = generate_answer(question)

            print("\n" + "=" * 80)
            print("FINAL ANSWER")
            print("=" * 80)
            print(answer)
            print("=" * 80)

        except Exception as e:

            print("\nError:")
            print(str(e))