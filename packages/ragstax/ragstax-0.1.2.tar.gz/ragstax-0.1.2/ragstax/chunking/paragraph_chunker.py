from typing import List
from nltk.tokenize import word_tokenize
from .base import BaseChunker
import nltk

nltk.download('punkt')

class ParagraphChunker(BaseChunker):
    def __init__(self, max_tokens: int = 200):
        self.max_tokens = max_tokens

    def chunk(self, text: str) -> List[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 20]
        chunks = []

        for para in paragraphs:
            tokens = word_tokenize(para)
            for i in range(0, len(tokens), self.max_tokens):
                chunk_tokens = tokens[i:i + self.max_tokens]
                chunk_text = " ".join(chunk_tokens)
                chunks.append(chunk_text)

        return chunks