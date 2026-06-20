from pathlib import Path
from pypdf import PdfReader

POLICY_FOLDER = Path("data/policies")


def load_documents():
    documents = []

    pdf_files = list(POLICY_FOLDER.glob("*.pdf"))

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()

            if text:
                documents.append(
                    {
                        "source": pdf_file.name,
                        "page": page_num + 1,
                        "content": text
                    }
                )

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"Loaded {len(docs)} pages")

    if docs:
        print("\nFirst document preview:\n")
        print(docs[0]["content"][:500])