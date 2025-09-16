from typing import List, Tuple
import numpy as np

def reciprocal_rank_fusion(fts_results: List[Tuple[int, float]],
                          vector_results: List[Tuple[int, float]],
                          k: int = 60) -> List[Tuple[int, float]]:
    """Merge FTS and vector search results using RRF."""
    scores = {}

    # Add FTS scores
    for rank, (doc_id, _) in enumerate(fts_results, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)

    # Add vector scores
    for rank, (doc_id, _) in enumerate(vector_results, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)

    # Sort by combined score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
