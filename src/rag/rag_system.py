import logging

from src.rag import extractor, embedder, retriever
from src.config import *

logger = logging.getLogger(__name__)


class RagSystem:
    def __init__(
            self,
            filepath,
            chunk_size,
            chunk_overlap,
            separators,
            embedding_model,
            database_url,
            top_k
    ):
        logger.info("-> Inizializzazione RagSystem")
        self.extractor = extractor.Extractor(filepath, chunk_size, chunk_overlap, separators)
        self.embedder  = embedder.Embedder(embedding_model, database_url)
        self.retriever = retriever.Retriever(embedding_model, top_k)
        logger.info("RagSystem inizializzato")

    def initialize_rag(self):
        chunks = self.extractor.chunk_text()
        collection = self.embedder.build_index(chunks)
        logger.info(f"RAG pronto | {collection.count()} chunk indicizzati")
        return collection
