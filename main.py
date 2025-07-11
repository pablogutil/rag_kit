from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from unstructured.partition.pdf import partition_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

app = FastAPI()

def load_pdf(file_path: str) -> str:
    elements = partition_pdf(file_path)
    return "\n\n".join([str(element) for element in elements])

def split_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def get_embeddings():
    return OpenAIEmbeddings()

def get_qdrant_vectorstore(collection_name: str):
    client = QdrantClient(url="http://localhost:6333")
    return Qdrant(client, collection_name, embeddings=get_embeddings())

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        text = load_pdf(tmp_file_path)
        chunks = split_text(text)
        
        vectorstore = get_qdrant_vectorstore("default")
        vectorstore.add_texts(chunks)
        
        return {"message": "PDF uploaded and processed successfully", "chunks_count": len(chunks)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        os.unlink(tmp_file_path)

@app.get("/query/")
async def query_documents(q: str):
    try:
        vectorstore = get_qdrant_vectorstore("default")
        results = vectorstore.similarity_search(q, k=5)
        
        return {
            "query": q,
            "results": [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))