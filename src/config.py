import logging

# Ollama Config
API_URL = "http://localhost:11434"

# Chat Model Config
MODEL = "llama3.2:latest"
TEMPERATURE = 0.1
TOP_P = 0.1
NUM_PREDICT = 200

# Embedding Model Config
EMBEDDING_MODEL = "nomic-embed-text"
TOP_K = 5

# Extractor Config
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# File Config
FILE_PATH = "./data/Manuale_Gestione_SIARB.pdf"
SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n", " "]

# Database Config
DATABASE_URL = "./data/chroma/chroma.db"

# Memory Config
MEMORY_TOP_K = 3
MEMORY_WINDOW_SIZE = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
