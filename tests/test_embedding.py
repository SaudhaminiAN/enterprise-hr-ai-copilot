from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embedding...")

embedding = model.encode("Hello world")

print("Embedding Length:", len(embedding))
print("Success!")