def reciprocal_rank_fusion(
    dense_results,
    bm25_results,
    k=60
):

    scores = {}
    docs = {}

    for rank, row in enumerate(
        dense_results,
        start=1
    ):

        doc_id = row[0]

        scores[doc_id] = (
            scores.get(doc_id, 0)
            + 1 / (k + rank)
        )

        docs[doc_id] = row

    for rank, row in enumerate(
        bm25_results,
        start=1
    ):

        doc_id = row[0]

        scores[doc_id] = (
            scores.get(doc_id, 0)
            + 1 / (k + rank)
        )

        docs[doc_id] = row

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        docs[doc_id]
        for doc_id, _
        in ranked
    ]