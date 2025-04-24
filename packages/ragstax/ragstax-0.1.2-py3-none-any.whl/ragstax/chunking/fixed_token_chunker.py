from transformers import AutoTokenizer
from ragstax.chunking.base import BaseChunker
from typing import List
import nltk

nltk.download('punkt')

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

class FixedTokenChunker(BaseChunker):
    def __init__(self, max_tokens: int = 1000, overlap: int = 250):
        self.max_tokens = max_tokens
        self.overlap = overlap
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def chunk(self, text: str) -> List[str]:
        tokens = self.tokenizer.tokenize(text)
        chunks = []
        i = 0
        while i < len(tokens):
            chunk_tokens = tokens[i:i + self.max_tokens]
            chunk = self.tokenizer.convert_tokens_to_string(chunk_tokens)
            chunks.append(chunk)
            i += self.max_tokens - self.overlap
        return chunks
