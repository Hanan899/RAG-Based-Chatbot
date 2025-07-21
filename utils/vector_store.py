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

def query_vector_store(user_query, k=5, return_docs=True, relevance_threshold=0.5):
    print("🚀 Starting query_vector_store()")
    print(f"📨 Incoming query: {user_query}")
    print(f"⚙️ Top k = {k}, Return Docs = {return_docs}, Relevance Threshold = {relevance_threshold}")
    
    print("📦 Loading vector store...")
    db = load_vector_store()
    print("✅ Vector store loaded.")

    results_final = []
    print(f"📂 Initialized empty results list: {results_final}")
    
    if len(user_query) > 1000:
        print(f"✂️ Query length = {len(user_query)} > 1000, splitting query...")
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        query_chunks = splitter.split_text(user_query)
        print(f"🔍 Query split into {len(query_chunks)} chunks.")
    else:
        query_chunks = [user_query]
        print(f"🔍 Query is short. Using 1 chunk: {query_chunks}")

    all_scores = []
    print("📊 Starting similarity search for each query chunk...")

    for i, chunk in enumerate(query_chunks):
        print(f"🔍 Searching vector store for chunk {i+1}/{len(query_chunks)}: {chunk[:100]}...")
        results = db.similarity_search_with_score(chunk, k=k)
        print(f"📈 Chunk {i+1} returned {len(results)} results with scores:")

        for doc, score in results:
            all_scores.append(score)
            print(f"   📌 Score: {score:.4f}")
            if return_docs:
                results_final.append(doc.page_content)
                print(f"   📄 Content snippet: {doc.page_content[:300]}")
            else:
                results_final.append({
                    "chunk": chunk,
                    "score": score,
                    "content": doc.page_content[:300]
                })

    print(f"📊 All scores collected: {all_scores}")
    print(f"📦 Total results collected: {len(results_final)}")

    if return_docs:
        print("🧪 Filtering results based on relevance threshold...")
        if not results_final:
            print("⚠️ No results found.")
            return []
        elif all(s <= relevance_threshold for s in all_scores):
            print(f"❌ All scores <= {relevance_threshold} — considered irrelevant. Returning empty list.")
            return []
        else:
            print(f"✅ Returning {len(results_final)} relevant documents.")
            return results_final
    else:
        print(f"✅ Returning {len(results_final)} results with metadata.")
        return results_final
