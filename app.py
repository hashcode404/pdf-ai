
import os
import tempfile
import streamlit as st

from pdf_rag import process_pdf, ask_question


# Page configuration
st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF AI Assistant")
st.caption("Ask questions about your PDF using AI.")

# Session state
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    st.header("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if st.button("Process PDF", use_container_width=True):

        if uploaded_file is None:
            st.warning("Please upload a PDF first.")

        else:
            try:
                with st.spinner("Processing PDF..."):

                    # Save uploaded PDF temporarily
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            uploaded_file.getvalue()
                        )

                        file_path = temp_file.name

                    # Process PDF and store embeddings
                    process_pdf(file_path)

                    st.session_state.pdf_path = file_path
                    st.session_state.pdf_name = uploaded_file.name
                    st.session_state.messages = []

                st.success("PDF processed successfully!")

            except Exception as error:
                st.error(f"Processing failed: {error}")

    if st.session_state.pdf_name:
        st.info(f"Current PDF: {st.session_state.pdf_name}")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []


# Chat interface
if st.session_state.pdf_path:

    st.subheader("Chat with your PDF")

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Question input
    question = st.chat_input(
        "Ask something about your PDF..."
    )

    if question:

        # Display user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Generate AI answer
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    answer, sources = ask_question(
                        question,
                        st.session_state.pdf_path
                    )

                    st.markdown(answer)

                    if sources:
                        unique_pages = sorted(
                            set(sources)
                        )

                        st.caption(
                            "Sources: " +
                            ", ".join(
                                f"Page {page}"
                                for page in unique_pages
                            )
                        )

                except Exception as error:
                    answer = f"Something went wrong: {error}"
                    st.error(answer)

        # Save answer
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

else:
    st.info(
        "Upload and process a PDF to start chatting."
    )
