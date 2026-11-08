
import fitz

# Open the PDF file
pdf = fitz.open("Pranav_.pdf")

# Loop through pages using page count
for page_number in range(pdf.page_count):
    page = pdf.load_page(page_number)

    text = page.get_text()

    print(f"\n--- Page {page_number + 1} ---")
    print(text)

# Close the PDF
pdf.close()
