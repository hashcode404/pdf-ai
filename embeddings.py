
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "How can I reset my password?",
    "How do I recover my account?",
    "Python is a programming language."
]

embeddings = model.encode(sentences, convert_to_tensor=True)

# Compare sentence 1 with sentence 2
similarity_1 = util.cos_sim(embeddings[0], embeddings[1])

# Compare sentence 1 with sentence 3
similarity_2 = util.cos_sim(embeddings[0], embeddings[2])

print("Password similarity:", similarity_1.item())
print("Password vs Python similarity:", similarity_2.item())
