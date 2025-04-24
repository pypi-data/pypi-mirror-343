from typing import List
from nltk.tokenize import sent_tokenize
from .base import BaseChunker
import nltk

nltk.download('punkt')

class SentenceChunker(BaseChunker):
    def __init__(self, max_sentences: int = 3):
        self.max_sentences = max_sentences

    def chunk(self, text: str) -> List[str]:
        sentences = sent_tokenize(text)
        chunks = []
        for i in range(0, len(sentences), self.max_sentences):
            chunks.append(" ".join(sentences[i:i + self.max_sentences]))
        return chunks
