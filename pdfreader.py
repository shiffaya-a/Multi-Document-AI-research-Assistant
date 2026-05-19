from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdfpath):
    reader=PdfReader(pdfpath)
    content=[]
    for page_number,page in enumerate(reader.pages,start=1):
        text=page.extract_text()
        if text:
            content.append({"page":page_number,"text":text})
    return content

def convert_text_chunks(text,chunk_size=900,overlap=150):
    chunks=[]
    start=0
    while start <len(text):
        end=start+chunk_size
        chunk=text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start=end-overlap
    return chunks

def create_documents_chunks(pdfpath):
    pages=extract_text_from_pdf(pdfpath)
    file_name=Path(pdfpath).name

    all_chunks=[]
    for page in pages:
        chunks = convert_text_chunks(page['text'])
        for chunk_index,chunk in enumerate(chunks,start=1):
            all_chunks.append(
            { "source":file_name,
              "page_number":page['page'],
              "page_chunk_id":chunk_index,
              "pages_chunk":chunk

            })
    return all_chunks

def create_chunks_from_multiple_pdfs(pdf_path):
    all_chunks=[]
    for pdf in pdf_path:
        chunks=create_documents_chunks(pdf)
        all_chunks.extend(chunks)
    return all_chunks