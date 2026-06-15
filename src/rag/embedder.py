import logging

import ollama
import chromadb

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self, model, db_path: str = None):
        self.model = model
        self.db_path = db_path
        logger.info(f"Embedder pronto | model={model} | db_path={db_path}")

    def embed(self, texts: list) -> list:
        embeddings = []
        for i, t in enumerate(texts):
            emb = ollama.embeddings(model=self.model, prompt=t)["embedding"]
            embeddings.append(emb)

        return embeddings

    def build_index(self, chunks: list) -> object:
        if not self.db_path:
            raise ValueError("Database path must be provided")

        client = chromadb.PersistentClient(path=self.db_path)
        collection = client.get_or_create_collection("db_data")

        embeddings = self.embed(chunks)

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )
        return collection
