import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

CHROMA_PATH = "chroma"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(chunks):
    CHROMA_PATH  = "chroma"
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma",
    collection_name="rag-data"
)
    return db

def load_vector_store():
    db = Chroma(
        collection_name="rag-data",
        persist_directory="chroma",
        embedding_function=embeddings
    )
    return db

def add_to_vector_store(chunks):
    db = load_vector_store()
    db.add_documents(chunks)
    return db

def query_vector_store(user_query, k=5, return_docs=False):
    db = load_vector_store()
    results_final = []
    
    if len(user_query) > 1000:
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        query_chunks = splitter.split_text(user_query)
    else:
        query_chunks = [user_query]

    for i, chunk in enumerate(query_chunks):
        results = db.similarity_search_with_score(chunk, k=k)
        for doc, score in results:
            if return_docs:
                results_final.append(doc.page_content)
            else:
                results_final.append({
                    "chunk": chunk,
                    "score": score,
                    "content": doc.page_content[:300]
                })
    
    return results_final

