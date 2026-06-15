from app.retrieval.dense_search import dense_search
from app.retrieval.bm25_search import bm25_search
from app.fusion.rrf import reciprocal_rank_fusion

TOP_K = 5


def hybrid_search(query):

    dense_results = dense_search(
        query,
        top_k=20
    )

    bm25_results = bm25_search(
        query,
        top_k=20
    )

    fused_results = reciprocal_rank_fusion(
        dense_results,
        bm25_results
    )

    return fused_results[:TOP_K]