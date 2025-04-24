from transformers import AutoTokenizer
from typing import List
import nltk

nltk.download('punkt')

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def fixed_token_chunking(text: str, max_tokens: int = 1000, overlap: int = 250) -> List[str]:
    tokens = tokenizer.tokenize(text)
    chunks = []
    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk)
        i += max_tokens - overlap
    return chunks
