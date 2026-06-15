import logging

import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_SIZE, CHUNK_OVERLAP, FILE_PATH, SEPARATORS

logger = logging.getLogger(__name__)


class Extractor:
    def __init__(
            self,
            pdf_path: str = FILE_PATH,
            chunk_size: int = CHUNK_SIZE,
            chunk_overlap: int = CHUNK_OVERLAP,
            separators: list = SEPARATORS
    ):
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators

        logger.info(f"Extractor pronto | file={pdf_path} | chunk_size={chunk_size} | overlap={chunk_overlap}")

    def extract_text(self) -> str:
        text = pymupdf4llm.to_markdown(self.pdf_path)
        return text

    def chunk_text(self) -> list:
        text = self.extract_text()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators
        )

        chunks = splitter.split_text(text)
        
        return chunks
