import os

from dotenv import load_dotenv

load_dotenv()

# ==============================
# Gemini Configuration
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# ==============================
# Embedding Model
# ==============================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==============================
# ChromaDB
# ==============================

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "hr_policies"

# ==============================
# Search
# ==============================

TOP_K = 3