import chromadb
from sentence_transformers import SentenceTransformer




def create_vector_store(chunks,db_path="chroma_db"):
    client=chromadb.PersistentClient(path=db_path)
    collection=client.get_or_create_collection(name="research_papers")
    model=SentenceTransformer("all-MiniLM-L6-v2")
    ids=[]
    documents=[]
    meta_datas=[]
    embeddings=[]
    for index,chunk in enumerate(chunks):
        chunk_id = f"{chunk['source']}_page_{chunk['page_number']}_chunk_{chunk['page_chunk_id']}"
        ids.append(chunk_id)
        documents.append(chunk["pages_chunk"])
        meta_datas.append({"source":chunk["source"],
                          "page_number":chunk["page_number"],
                          "page_chunk_id":chunk["page_chunk_id"]})
        embedding=model.encode(chunk["pages_chunk"],normalize_embeddings=True).tolist()
        embeddings.append(embedding)
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=meta_datas,
        embeddings=embeddings
    )
    return collection