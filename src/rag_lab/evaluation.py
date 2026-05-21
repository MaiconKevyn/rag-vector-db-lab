def recall_at_k(expected_ids: list[str], retrieved_ids: list[str], k: int) -> float:
    if not expected_ids:
        return 0.0
    retrieved = set(retrieved_ids[:k])
    expected = set(expected_ids)
    return len(expected & retrieved) / len(expected)


def reciprocal_rank(expected_ids: list[str], retrieved_ids: list[str]) -> float:
    expected = set(expected_ids)
    for position, retrieved_id in enumerate(retrieved_ids, start=1):
        if retrieved_id in expected:
            return 1.0 / position
    return 0.0
