from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from abc import ABC, abstractmethod

import httpx


class EmbeddingProvider(ABC):
    provider: str
    model: str
    dimension: int
    preprocessing_version = "canonical-text-v1"

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class DeterministicHashEmbeddingProvider(EmbeddingProvider):
    provider = "local"
    preprocessing_version = "canonical-text-v1"

    _concepts = {
        "safety": {"safe", "safety", "guardrail", "policy", "untrusted", "instruction"},
        "chunking": {"chunk", "chunking", "fragment", "overlap", "boundary", "context"},
        "embedding": {"embedding", "vector", "dimension", "model", "provider", "semantic"},
        "citation": {"citation", "source", "provenance", "evidence", "locator", "resolve"},
        "search": {"search", "retrieval", "query", "rank", "similarity", "result"},
    }

    def __init__(self, dimension: int = 128, model: str = "deterministic-hash-v1") -> None:
        self.dimension = dimension
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        tokens = self._tokens(text)
        features: list[tuple[str, float]] = [(token, 1.0) for token in tokens]
        features.extend(
            (f"pair:{left}:{right}", 0.45) for left, right in zip(tokens, tokens[1:], strict=False)
        )
        token_set = set(tokens)
        for concept, vocabulary in self._concepts.items():
            if token_set.intersection(vocabulary):
                features.append((f"concept:{concept}", 1.6))

        vector = [0.0] * self.dimension
        for feature, weight in features:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=16).digest()
            index = int.from_bytes(digest[:8], "big") % self.dimension
            sign = 1.0 if digest[8] & 1 else -1.0
            vector[index] += sign * weight
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [round(value / norm, 10) for value in vector]

    @staticmethod
    def _tokens(text: str) -> list[str]:
        folded = unicodedata.normalize("NFKD", text.casefold())
        ascii_text = "".join(char for char in folded if not unicodedata.combining(char))
        return re.findall(r"[a-z0-9]{2,}", ascii_text)


class OpenAICompatibleEmbeddingProvider(EmbeddingProvider):
    provider = "openai-compatible"
    preprocessing_version = "canonical-text-v1"

    def __init__(self, base_url: str, api_key: str, model: str, dimension: int) -> None:
        if not base_url or not api_key or not model:
            raise ValueError("OpenAI-compatible provider requires URL, API key and model")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = httpx.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "input": texts, "dimensions": self.dimension},
            timeout=20,
        )
        response.raise_for_status()
        vectors = [item["embedding"] for item in response.json()["data"]]
        if any(len(vector) != self.dimension for vector in vectors):
            raise ValueError("embedding provider returned an incompatible dimension")
        return vectors


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(f"{value:.10f}" for value in values) + "]"
