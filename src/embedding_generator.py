from sentence_transformers import SentenceTransformer
from text_chunker import chunk_documents


def generate_embeddings():

    chunks = chunk_documents()

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print(f"Total Chunks: {len(chunks)}")
    print(f"Embedding Shape: {embeddings.shape}")

    return chunks, embeddings


if __name__ == "__main__":
    generate_embeddings()