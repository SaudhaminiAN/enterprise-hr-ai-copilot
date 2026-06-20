from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_documents


def chunk_documents():
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for doc in documents:
        split_text = splitter.split_text(doc["content"])

        for idx, chunk in enumerate(split_text):
            chunks.append(
                {
                    "content": chunk,
                    "source": doc["source"],
                    "page": doc["page"],
                    "chunk_id": idx
                }
            )

    return chunks


if __name__ == "__main__":
    chunks = chunk_documents()

    print(f"Total Chunks: {len(chunks)}")

    if chunks:
        print("\nSample Chunk:\n")
        print(chunks[0]["content"][:500])