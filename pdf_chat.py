
import os
import fitz

from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Read PDF
def read_pdf(file_path):
    pdf = fitz.open(file_path)

    full_text = ""

    for page_number in range(pdf.page_count):
        page = pdf.load_page(page_number)
        page_text = page.get_text("text")

        if isinstance(page_text, str):
            full_text += page_text

    pdf.close()

    return full_text


# Ask AI about PDF
def ask_question(pdf_text, question):

    prompt = f"""
    You are a PDF assistant.

    Answer the question using ONLY the information
    available in the following document.

    If the answer is not available, say:
    "I couldn't find this information in the PDF."

    DOCUMENT:
    {pdf_text}

    QUESTION:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# Main program
if __name__ == "__main__":

    pdf_text = read_pdf("Pranav_P.pdf")

    print("PDF loaded successfully!")
    print("Ask questions about your PDF.")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        answer = ask_question(pdf_text, question)

        print("\nAI:", answer)
