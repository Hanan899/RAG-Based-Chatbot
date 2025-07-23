from fastapi import FastAPI, UploadFile, File
from utils.document_loader import process_pdf_bytes
from utils.text_splitter import split_documents
from utils.vector_store import add_to_vector_store, query_vector_store
import base64
from utils.llm import generate_answer_from_gemini
from utils.web_search_tavily import web_search_structured_answer

app = FastAPI()
CHROMA_PATH = "chroma"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    encoded_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    decoded_bytes = base64.b64decode(encoded_b64)
    print(f"📥 Received file: {file.filename}")

    # Process in memory from base64 stream
    doc = process_pdf_bytes(decoded_bytes, file.filename)
    chunks = split_documents(doc)
    add_to_vector_store(chunks)

    return {
        "message": f"{file.filename} uploaded, base64-decoded, OCR-processed, and embedded.",
        "size_original_bytes": len(pdf_bytes),
        "size_base64": len(encoded_b64),
        "size_decoded_bytes": len(decoded_bytes)
    }



@app.post("/chat/")
async def chat_with_llm(query: str):
    try:
        # Step 1: Try RAG vector store
        docs = query_vector_store(query, return_docs=True)
        if docs:
            context = "\n\n".join([doc["content"] for doc in docs])
            answer = generate_answer_from_gemini(query, context)

            # Prepare source references from metadata
            sources = []
            for doc in docs:
                meta = doc.get("metadata", {})
                filename = meta.get("source", "Unknown file")
                page = meta.get("page_number", "?")
                line = meta.get("line_number", "?")
                sources.append(f"{filename} → Page {page}, Line {line}")

            #Correct order
            if answer is None:
                answer = web_search_structured_answer(query)
                source = "Answer from web search + Gemini"
            else:
                source = "Answer from PDF using RAG\n" + "\n".join(sources)

        else:
            answer = web_search_structured_answer(query)
            source = "Answer from web search + Gemini"

        return {
            "answer": answer,
            "source": source,
            "tokens": len(answer.split()) if isinstance(answer, str) else 0
        }

    except Exception as e:
        return {
            "answer": f"❌ Unexpected error: {str(e)}",
            "source": "⚠️ None",
            "tokens": 0
        }
