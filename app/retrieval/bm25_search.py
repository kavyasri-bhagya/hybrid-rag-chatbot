import pickle
from pathlib import Path

INDEX_FILE = Path(
    "data/bm25/bm25.pkl"
)


def bm25_search(query, top_k=20):

    with open(
        INDEX_FILE,
        "rb"
    ) as f:

        data = pickle.load(f)

    bm25 = data["bm25"]
    metadata = data["metadata"]

    scores = bm25.get_scores(
        query.lower().split()
    )

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for idx, score in ranked[:top_k]:

        doc = metadata[idx]

        results.append(
            (
                doc["id"],
                doc["file_name"],
                doc["chunk_id"],
                doc["chunk_text"],
                float(score)
            )
        )

    return results