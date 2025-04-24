"""KNO-SDK — clone, index and search GitHub repos via Chroma embeddings."""

__version__ = "0.1.1"

from .indexer import clone_and_index, search, RepoIndex, EmbeddingMethod, agent_query

__all__ = [
    "clone_and_index",
    "search",
    "RepoIndex",
    "EmbeddingMethod",
    "agent_query"
]