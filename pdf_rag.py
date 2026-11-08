
import os
import fitz
import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai

# -----------------------------
# 1. Configuration
# -----------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

db_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = db_client.get_or_create_collection(
    name="pdf_rag_assistant"
)


# -----------------------------
# 2. Read PDF
# -----------------------------

def read_pdf(file_path):

    pdf = fitz.open(file_path)

    pages = []

    for page_number in range(pdf.page_count):

        page = pdf.load_page(page_number)
        text = page.get_text("text")

        if isinstance(text, str) and text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    pdf.close()

    return pages


# -----------------------------
# 3. Split text into chunks
# -----------------------------

def split_into_chunks(text, chunk_size=500, overlap=50):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# -----------------------------
# 4. Process and store PDF
# -----------------------------

def process_pdf(file_path):

    pages = read_pdf(file_path)

    documents = []
    ids = []
    metadatas = []

    for page in pages:

        chunks = split_into_chunks(page["text"])

        for index, chunk in enumerate(chunks):

            documents.append(chunk)

            ids.append(
                f"page-{page['page']}-chunk-{index}"
            )

            metadatas.append({
                "page": page["page"],
                "source": file_path
            })

    if not documents:
        raise ValueError("No readable text found in PDF.")

    # Remove previous chunks from this PDF
    collection.delete(
        where={"source": file_path}
    )

    # Generate embeddings
    embeddings = embedding_model.encode(
        documents
    ).tolist()

    # Store in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Processed {len(documents)} chunks!")


# -----------------------------
# 5. Search relevant PDF chunks
# -----------------------------

def search_pdf(question, file_path):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    # Count chunks belonging to this PDF
    existing_chunks = collection.get(
        where={"source": file_path},
        include=[]
    )

    total_chunks = len(existing_chunks["ids"])

    if total_chunks == 0:
        return "", []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(4, total_chunks),
        where={"source": file_path}
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    if documents is None or not documents[0]:
        return "", []

    context_parts = []
    sources = []

    for index, document in enumerate(documents[0]):

        metadata = metadatas[0][index] if metadatas else {}

        page_number = metadata.get("page", "Unknown")

        context_parts.append(
            f"[Page {page_number}]\n{document}"
        )

        sources.append(page_number)

    return "\n\n".join(context_parts), sources



# -----------------------------
# 6. Ask Gemini
# -----------------------------

def ask_question(question, file_path):

    context, sources = search_pdf(question, file_path)

    if not context:
        return "No relevant information found in the PDF.", []

    prompt = f"""
    You are a helpful PDF assistant.

    Answer using only the provided document context.

    If the answer is unavailable, say you couldn't
    find the information in the document.

    Include page references when possible.

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text or "No response generated.", sources


# -----------------------------
# 7. Main application
# -----------------------------

if __name__ == "__main__":

    pdf_path = "Pranav_P.pdf"

    print("Loading PDF...")

    process_pdf(pdf_path)

    print("\nPDF AI Assistant is ready!")
    print("Ask questions about your document.")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(question, pdf_path)

        print("\nAI:", answer)
