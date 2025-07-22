from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os
import logging
from lexie.config import VECTOR_INDEX_PATH as DB_PATH


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
logging.basicConfig(level=logging.INFO)

def hybrid_search(query: str, k: int = 3):
    if not os.path.exists(DB_PATH):
        logging.warning("❌ FAISS index not found at %s", DB_PATH)
        return []

    db = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    docs = db.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]