import os, json
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from src.templates import OWN_FUNDS_SCHEMA, SYSTEM_PROMPT

load_dotenv()

def run_query(user_scenario):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
   
    vector_db = FAISS.load_local("vector_db/pra_index", embeddings, allow_dangerous_deserialization=True)
    
    docs = vector_db.similarity_search(user_scenario, k=6) 
    
    context_text = "\n\n".join([
        f"DOC: {d.metadata['source']} | PAGE: {d.metadata['page']}\n{d.page_content}" 
        for d in docs
    ])
    
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt = SYSTEM_PROMPT.format(
        user_scenario=user_scenario,
        context=context_text,
        schema=json.dumps(OWN_FUNDS_SCHEMA)
    )
    
    return llm.invoke(prompt).content