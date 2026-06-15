import logging

import ollama

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, model_name: str, top_k: int):
        self.model_name = model_name
        self.top_k = top_k
        logger.info(f"Retriever pronto | model={model_name} | top_k={top_k}")

    def search(self, query: str, collection) -> dict:
        query_embedding = ollama.embeddings(model=self.model_name, prompt=query)["embedding"]

        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k
        )

        return result
