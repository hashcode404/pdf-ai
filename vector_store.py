
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create local ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="pdf_documents"
)

# Sample document chunks
chunks = [
    "Python is a popular programming language.",
    "Flutter is used to build cross-platform mobile applications.",
    "AI agents can perform tasks using tools.",
    "Machine learning allows computers to learn from data."
]

# Generate embeddings
embeddings = model.encode(chunks).tolist()

# Store chunks and embeddings
collection.add(
    ids=["1", "2", "3", "4"],
    documents=chunks,
    embeddings=embeddings
)

print("Documents stored successfully!")
