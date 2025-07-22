# === FILE: utils/document_qa.py ===
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from lexie.config import LEXIE_PROMPT # ✅ Load from .env
from lexie.config import VECTOR_INDEX_PATH

import os
import tempfile
import shutil

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_pdf_to_faiss(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    vectordb = FAISS.from_documents(docs, embedding_model)

    print("🔄 Resetting FAISS index folder...")
    if os.path.exists(VECTOR_INDEX_PATH):
        shutil.rmtree(VECTOR_INDEX_PATH)
        print("🗑️ Deleted old index folder")

    os.makedirs(VECTOR_INDEX_PATH, exist_ok=True)
    vectordb.save_local(VECTOR_INDEX_PATH)
    print(f"📁 FAISS index saved at: {VECTOR_INDEX_PATH}")
    return vectordb

def load_faiss_index():
    if not os.path.exists(VECTOR_INDEX_PATH):
        raise FileNotFoundError("FAISS index not found")
    return FAISS.load_local(VECTOR_INDEX_PATH, embeddings=embedding_model, allow_dangerous_deserialization=True)

def handle_uploaded_pdf(filename: str, content: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        embed_pdf_to_faiss(tmp_path)
        return f"✅ File '{filename}' processed and embedded successfully."
    except Exception as e:
        return f"❌ Failed to process '{filename}': {str(e)}"
    finally:
        os.remove(tmp_path)

if __name__ == "__main__":
    print("✅ handle_uploaded_pdf is defined:", callable(handle_uploaded_pdf))
