# Multi-Document AI Research Assistant

A Streamlit-based research assistant that lets users upload multiple PDF research papers, build a searchable vector library, and ask questions with source citations.

## Features

- Upload and process multiple PDF papers
- Split documents into searchable text chunks
- Store embeddings in a persistent ChromaDB vector database
- Route questions between document-based RAG answers and general answers
- Rewrite follow-up questions into standalone questions
- Generate answers using retrieved document context
- Display source citations with file name and page number
- Maintain chat history during the Streamlit session
- Clear chat history or reset the full document library

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- PDF processing utilities
- LLM-based answer generation

## Project Structure

```text
.
├── app.py
├── pdfreader.py
├── vector_store.py
├── query_rewriter.py
├── query_router.py
├── llm_answer.py
├── memory.py
├── uploads/
├── chroma_db/
└── README.md
```

## How It Works

1. Upload one or more PDF research papers from the sidebar.
2. Click **Process PDFs** to extract text, create chunks, generate embeddings, and store them in ChromaDB.
3. Ask questions in the chat input.
4. The query router decides whether the question should use document retrieval or a general answer.
5. For document questions, the app retrieves the most relevant chunks and generates an answer with citations.
6. Sources are shown under the assistant response.

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not included yet, install the main dependencies:

```bash
pip install streamlit chromadb sentence-transformers pdfreader
```

Add any required LLM provider dependencies or API keys based on your `llm_answer.py` implementation.

## Running the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Usage

1. Upload PDF research papers using the sidebar.
2. Click **Process PDFs**.
3. Ask research questions in the chat box.
4. Expand **Sources** under an answer to view citations.
5. Use **Clear Chat** to reset only the conversation.
6. Use **Clear Library** to delete uploaded PDFs and the local ChromaDB database.

## Notes

- Uploaded PDFs are stored locally in the `uploads/` directory.
- Vector data is stored locally in the `chroma_db/` directory.
- These generated folders should usually be excluded from Git.
- The default embedding model is `all-MiniLM-L6-v2`.

## Suggested `.gitignore`

```gitignore
.venv/
__pycache__/
.DS_Store
uploads/
chroma_db/
*.pyc
```


