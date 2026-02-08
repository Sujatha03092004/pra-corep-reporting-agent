import os
import pdfplumber
from dotenv import load_dotenv
from langchain_core.documents import Document                
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def run_ingestion():
    raw_path = "data/raw/"
    docs = []
    
    for filename in os.listdir(raw_path):
        if filename.endswith(".pdf"):
            print(f"Reading {filename}...")
            with pdfplumber.open(os.path.join(raw_path, filename)) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        docs.append(Document(
                            page_content=text,
                            metadata={"source": filename, "page": i + 1}
                        ))

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    print("Loading local Hugging Face model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("vector_db/pra_index")
    print("Success! Local index saved to vector_db/pra_index")

if __name__ == "__main__":
    run_ingestion()