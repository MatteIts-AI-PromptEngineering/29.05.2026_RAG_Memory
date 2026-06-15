import logging

import ollama
import chromadb

logger = logging.getLogger(__name__)


class MemorySystem:

    COLLECTION_NAME = "conversation_memory"

    def __init__(self, embedding_model: str, database_url: str, top_k: int = 3, window_size: int = 10):
        self.model = embedding_model
        self.top_k = top_k
        self.window_size = window_size

        logger.info(f"Connessione MemorySystem a ChromaDB: {database_url}")
        client = chromadb.PersistentClient(path=database_url)
        self.collection = client.get_or_create_collection(self.COLLECTION_NAME)

        self._turn_count = self._load_turn_count()

        logger.info(
            f"MemorySystem pronto | collection='{self.COLLECTION_NAME}' | "
            f"turni in memoria={self._turn_count} | top_k={top_k} | window_size={window_size}"
        )

    def save_turn(self, user_msg: str, assistant_msg: str) -> None:
        turn_text = f"User: {user_msg}\nAssistant: {assistant_msg}"

        embedding = self._embed(turn_text)
        turn_id = f"turn_{self._turn_count}"

        self.collection.add(
            documents=[turn_text],
            embeddings=[embedding],
            ids=[turn_id],
            metadatas=[{"turn_index": self._turn_count}]
        )
        self._turn_count += 1

    def retrieve_relevant(self, query: str) -> list:
        total = self.collection.count()

        if total == 0:
            return []

        window_start = max(0, self._turn_count - self.window_size)
        n_results = min(self.top_k, total)

        query_kwargs = {
            "query_embeddings": [self._embed(query)],
            "n_results": n_results,
        }

        if window_start > 0:
            query_kwargs["where"] = {"turn_index": {"$gte": window_start}}

        result = self.collection.query(**query_kwargs)
        docs = result["documents"][0] if result["documents"] else []

        return docs


    def _embed(self, text: str) -> list:
        return ollama.embeddings(model=self.model, prompt=text)["embedding"]

    def _load_turn_count(self) -> int:
        total = self.collection.count()

        if total == 0:
            return 0

        results = self.collection.get(include=["metadatas"])
        indices = [res_record["turn_index"] for res_record in results["metadatas"]]
        max_idx = max(indices)

        return max_idx + 1
