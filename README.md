# PDF AI Assistant

An AI-powered PDF Question Answering application built with Python, Gemini, Sentence Transformers, and ChromaDB.

Upload a PDF, ask questions about its content, and get AI-generated answers based on relevant information retrieved from the document.

## Features

- Extract text from PDF documents.
- Split large documents into smaller text chunks.
- Generate text embeddings using Sentence Transformers.
- Store and retrieve document embeddings using ChromaDB.
- Perform semantic search to find relevant document sections.
- Generate context-aware answers using Google's Gemini API.
- Display answers based on the retrieved PDF content.

## Architecture

The application follows a Retrieval-Augmented Generation (RAG) workflow.

```text
              PDF Document
                   |
                   v
             Extract Text
                   |
                   v
             Text Chunking
                   |
                   v
          Generate Embeddings
                   |
                   v
             ChromaDB Store
                   |
                   |
       User Question
              |
              v
       Generate Query Embedding
              |
              v
       Semantic Search
              |
              v
       Retrieve Relevant Chunks
              |
              v
          Gemini API
              |
              v
         AI Generated Answer
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embedding generation |
| ChromaDB | Vector database |
| Google Gemini | AI-powered answer generation |
| python-dotenv | Environment variable management |

## Project Structure

```text
pdf-ai-assistant/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
├── sample.pdf
│
├── read_pdf.py
├── ask_ai.py
├── pdf_chat.py
├── embeddings.py
├── rag.py
├── vector_store.py
├── search_vectors.py
└── pdf_rag.py
```

## Prerequisites

- Python 3.10 or later
- pip
- Google Gemini API key

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pdf-ai-assistant.git

cd pdf-ai-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit your actual `.env` file or API key to GitHub.

### 5. Add a PDF document

Place a PDF file named `sample.pdf` in the project root.

## Usage

Run the complete PDF RAG application:

```bash
python pdf_rag.py
```

The application will:

1. Read the PDF document.
2. Extract its text.
3. Split the content into smaller chunks.
4. Generate embeddings.
5. Store the chunks in ChromaDB.
6. Accept questions through the terminal.
7. Retrieve relevant document sections.
8. Generate answers using Gemini.

### Example

```text
Loading PDF...
Processed 12 chunks!

PDF AI Assistant is ready!
Ask questions about your document.
Type 'exit' to stop.

You: What is this document about?

AI: This document explains...
```

## How RAG Works

Retrieval-Augmented Generation (RAG) combines information retrieval with an LLM.

Instead of sending an entire PDF to the AI model for every question:

1. The PDF is divided into smaller chunks.
2. Each chunk is converted into an embedding.
3. Embeddings are stored in ChromaDB.
4. The user's question is converted into an embedding.
5. ChromaDB retrieves semantically relevant chunks.
6. The retrieved content is passed to Gemini.
7. Gemini generates an answer using the provided context.

## Learning Objectives

This project was developed as a hands-on introduction to AI application development.

Concepts explored:

- Python fundamentals for AI development.
- Working with Large Language Models (LLMs).
- Prompt engineering.
- Text preprocessing and chunking.
- Vector embeddings.
- Cosine similarity.
- Vector databases.
- Semantic search.
- Retrieval-Augmented Generation (RAG).

## Future Improvements

- [ ] Streamlit web interface.
- [ ] Support multiple PDF uploads.
- [ ] Chat history and conversational memory.
- [ ] Display source page references.
- [ ] Support scanned PDFs using OCR.
- [ ] Improve chunking strategies.
- [ ] Add document management.
- [ ] Deploy as a web application.

## Security

- Keep API keys in environment variables.
- Never commit private documents or credentials.
- Keep local databases and virtual environments out of version control.

## License

This project is intended for learning and experimentation. Add an appropriate open-source license if you plan to distribute it publicly.
