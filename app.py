import streamlit as st
from pathlib import Path
from pdfreader import create_chunks_from_multiple_pdfs
from vector_store import create_vector_store
import chromadb
from sentence_transformers import SentenceTransformer
from query_rewriter import rewrite_question
from llm_answer import generate_answer,generate_general_answer
from memory import add_to_memory
from query_router import router_question
import shutil

st.set_page_config(
    page_title="Multi-Document Research Assistant",
    page_icon="📚",
    layout='wide'
)

st.title("Multi-document AI Research Assistant")
st.write("Upload research papers and ask questions with source citations.")
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
DB_PATH = BASE_DIR / "chroma_db"

uploaded_files=st.sidebar.file_uploader("Upload PDF Papers",
                                        type=['pdf'],
                                        accept_multiple_files=True)

if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} files(s) uploaded")
if st.sidebar.button("Process PDFs"):
    if not uploaded_files:
        st.sidebar.warning("Please upload the PDF files")
    else:
        pdf_paths=[]
        for uploaded_file in uploaded_files:
            file_path=UPLOAD_DIR/uploaded_file.name
            with open(file_path,"wb") as f:
                f.write(uploaded_file.getbuffer())
            pdf_paths.append(file_path)
        with st.spinner("Processing PDFs and creating vector database..."):
            chunks=create_chunks_from_multiple_pdfs(pdf_paths)
            collection = create_vector_store(chunks, db_path=str(DB_PATH))
        st.sidebar.success(f"Processed {len(chunks)} chunks from {len(pdf_paths)} PDF(s).")
        st.sidebar.write(f"Stored chunks: {collection.count()}")
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_messages = []
    st.rerun()
if st.sidebar.button("Clear Library"):
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)
    if DB_PATH.exists():
        shutil.rmtree(DB_PATH)
    UPLOAD_DIR.mkdir(exist_ok=True)
    st.session_state.chat_messages=[]
    st.sidebar.success("Library Cleared.Upload PDFs again")
    st.rerun()

st.divider()
st.subheader("Ask Questions")


for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(source)

question=st.chat_input("Please ask questions about the uploaded research papers")

if question:
    st.session_state.chat_messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)
    route = router_question(question)
    st.caption(f"Route: {route}")

    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(name="research_papers")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    if route == "RAG":
        standalone_question=rewrite_question(question)
        question_embedding=model.encode(
            standalone_question,
            normalize_embeddings=True
        ).tolist()
        results=collection.query(query_embeddings=[question_embedding],n_results=3)

        answer=generate_answer(standalone_question,results)
        sources = []


        for i, metadata in enumerate(results["metadatas"][0], start=1):
            sources.append(f"[{i}] {metadata['source']}, page {metadata['page_number']}")
    else:
        answer = generate_general_answer(question)
        sources = []
    with st.chat_message("assistant"):
        st.write(answer)
        if sources:
            with st.expander("Sources"):
                for source in sources:
                    st.write(source)

    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })

    add_to_memory(question,answer)
