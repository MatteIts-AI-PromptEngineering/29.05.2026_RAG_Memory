import gradio as gr

from src.rag.rag_system import RagSystem
from src.rag.memory_system import MemorySystem
from src.chat_client.client import Client
from src.chat_client.chat_engine import ChatEngine
from src.chat_client.prompt_builder import get_system_prompt
from src.config import (
    FILE_PATH, CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS,
    EMBEDDING_MODEL, DATABASE_URL, TOP_K,
    MODEL, API_URL, TEMPERATURE, TOP_P, NUM_PREDICT,
    MEMORY_TOP_K, MEMORY_WINDOW_SIZE,
)

rag = RagSystem(
    filepath=FILE_PATH,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=SEPARATORS,
    embedding_model=EMBEDDING_MODEL,
    database_url=DATABASE_URL,
    top_k=TOP_K,
)

file_collection = rag.initialize_rag()

memory = MemorySystem(
    embedding_model=EMBEDDING_MODEL,
    database_url=DATABASE_URL,
    top_k=MEMORY_TOP_K,
    window_size=MEMORY_WINDOW_SIZE,
)

client = Client(
    model=MODEL,
    api_url=API_URL,
    temperature=TEMPERATURE,
    top_p=TOP_P,
    num_predict=NUM_PREDICT,
    system_prompt=get_system_prompt(),
    window_size=MEMORY_WINDOW_SIZE,
)

engine = ChatEngine(
    kb_collection=file_collection,
    rag_system=rag,
    memory_system=memory,
    client=client,
)

# GRADIO
app = gr.ChatInterface(
    fn=engine.respond,
    title="JUST HIM",
    description=(
        "Fai domande, chill sicuramente ti so rispondere"
    ),
)

if __name__ == "__main__":
    app.launch()
