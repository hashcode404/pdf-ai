
from rag import split_into_chunks

text = """
Python is a programming language.
It is widely used in AI development.
AI agents can perform tasks automatically.
"""

chunks = split_into_chunks(text, chunk_size=10, overlap=2)

for index, chunk in enumerate(chunks):
    print(f"\nChunk {index + 1}:")
    print(chunk)
