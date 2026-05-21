from collections.abc import Iterable
from hashlib import sha256
from random import Random

from fastembed import TextEmbedding


class FastEmbedder:
    def __init__(self, model_name: str) -> None:
        self.model = TextEmbedding(model_name=model_name)

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        return [list(vector) for vector in self.model.embed(list(texts))]


class DeterministicEmbedder:
    def __init__(self, dimensions: int = 16) -> None:
        self.dimensions = dimensions

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            seed = int(sha256(text.encode("utf-8")).hexdigest(), 16)
            rng = Random(seed)
            vectors.append([rng.uniform(-1.0, 1.0) for _ in range(self.dimensions)])
        return vectors
