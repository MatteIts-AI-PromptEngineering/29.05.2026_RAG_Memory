import logging

from src.chat_client.prompt_builder import get_user_prompt

logger = logging.getLogger(__name__)


class ChatEngine:
    def __init__(self, kb_collection, rag_system, memory_system, client):
        self.kb_collection = kb_collection
        self.rag = rag_system
        self.memory = memory_system
        self.client = client
        logger.info("ChatEngine pronto")

    def respond(self, message, history: list) -> str:
        message = self._normalize(message)
        
        doc_results = self.rag.retriever.search(message, self.kb_collection)
        doc_chunks = doc_results["documents"][0]

        memory_chunks = self.memory.retrieve_relevant(message)

        prompt = get_user_prompt(doc_chunks, message, memory_chunks)

        answer = self.client.complete(prompt, history)

        self.memory.save_turn(message, answer)
        logger.info("Turno completato")

        return answer

    @staticmethod
    def _normalize(msg) -> str:
        # adattatore lista multimodale -> str [{'type': 'text', 'text': '...'}]

        if isinstance(msg, str):
            return msg

        if isinstance(msg, list):
            parts = []
            for part in msg:
                if isinstance(part, dict) and part.get("type") == "text":
                    parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    parts.append(part)
            normalized = " ".join(parts).strip()
            return normalized
        return str(msg)
