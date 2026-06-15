from pathlib import Path
from pypdf import PdfReader

PDF_FOLDER = Path("data/pdf")


def load_pdfs():
    documents = []

    for pdf_file in PDF_FOLDER.glob("*.pdf"):

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        documents.append(
            {
                "file_name": pdf_file.name,
                "text": text
            }
        )

    return documents

if __name__ == "__main__":
    docs = load_pdfs()
    for doc in docs:
        print("=" * 50)
        print(doc["file_name"])
        print(doc["text"][:1000])