
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="pdf_documents"
)

# User question
question = "How can I develop mobile applications?"

# Convert question into embedding
query_embedding = model.encode(question).tolist()

# Search database
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

# Display results

# Display results
documents = results["documents"]

if documents is not None and documents[0]:
    for document in documents[0]:
        print(document)
else:
    print("No matching documents found.")

