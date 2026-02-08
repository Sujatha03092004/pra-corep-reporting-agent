# PRA Regulatory Reporting Assistant (COREP Prototype)
An Agentic RAG-based AI designed to automate the interpretation of the PRA Rulebook 2025 and Annex II Reporting Instructions for COREP CA1 (Own Funds) reporting.

## Demo Link
https://pra-corep-reporting-agent-dnql8d3uvwbke4xkuwtekx.streamlit.app
(The fastest way to verify the Agent's reasoning and output quality live without local setup.)

## Overview
Regulatory reporting is labor-intensive and error-prone. This prototype demonstrates how an "Agentic" AI can:
- Retrieve specific articles from dense PDF regulations.
- Reason through accounting logic (Hierarchy, Aggregation, and Sign Conventions).
- Generate structured, audit-ready extracts aligned with PRA taxonomies.

## Key Features
- Logical Hierarchy: Understands the relationship between capital tiers (e.g., Own Funds = Tier 1 + Tier 2).
- Sign Convention Compliance: Automatically identifies deductions (e.g., Goodwill, Foreseeable Dividends) and reports them as negative values per Annex II instructions.
- Audit Log: Every value is mapped to a specific source_ref (e.g., Article 26 CRR) for full legal traceability.
- Deterministic Calculation: Uses temperature=0 and specific system prompting to ensure mathematical precision.

## Tech Stack
- LLM: Llama 3.3 70B (via Groq LPU)
- Vector DB: FAISS
- Framework: LangChain & Streamlit
- Embeddings: HuggingFace all-MiniLM-L6-v2

## Project Structure
- app.py: Main dashboard and robust JSON extraction logic.
- src/rag_engine.py: Reasoning loop and RAG retrieval logic.
- src/templates.py: Regulatory JSON schemas and system prompts.
- src/ingest.py: Document processor (PDF to Vector chunks).

## How to run locally
- **Step 1:** Download the zip folder onto your local computer and extract it. 
- **Step 2:** Create a virtual environment (preferably Python 3.10) and activate it: 
.venv/Scripts/activate # On Windows 
- **Step 3:** Create a .env file in the root directory and store your Groq API Key by pasting this line: GROQ_API_KEY=YOUR_API_KEY (Get your key at https://console.groq.com/) 
- **Step 4:** Run the command if you are adding more PDFs to `data/raw` or deleting the existing vector_db:
python src/ingest.py 
This will process the PDFs and create the vector_db folder.  
- **Step 5:** Run the command:
streamlit run app.py
The local web interface will open automatically.

**Disclaimer: The answers provided are solely based on the PRA Rulebook 2025 and Annex II Instructions in the demo prototype. Ensure to double check in any case AI may not generate 100% accurate values. Human verification is required for any actual regulatory submission.**
