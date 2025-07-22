# === test_vector_search.py ===
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

try:
    db = FAISS.load_local("data/faiss_index", embeddings=embedding_model)
    results = db.similarity_search("What is AI?", k=3)
    print("✅ FAISS Search Results:")
    for doc in results:
        print("-", doc.page_content)
except Exception as e:
    print("❌ FAISS error:", str(e))
