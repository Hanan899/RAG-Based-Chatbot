from fastapi import FastAPI, UploadFile, File
from utils.document_loader import process_pdf_bytes
from utils.text_splitter import split_documents
from utils.vector_store import add_to_vector_store, load_vector_store, query_vector_store
import base64
from utils.llm import generate_answer_from_gemini

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
    chunks = split_documents([doc])
    add_to_vector_store(chunks)

    return {
        "message": f"{file.filename} uploaded, base64-decoded, OCR-processed, and embedded.",
        "size_original_bytes": len(pdf_bytes),
        "size_base64": len(encoded_b64),
        "size_decoded_bytes": len(decoded_bytes)
    }

@app.post("/chat/")
async def chat_with_llm(query: str):
    docs = query_vector_store(query, return_docs=True)
    full_context = "\n\n".join(docs)
    
    # send full_context + query to Gemini here...
    response = generate_answer_from_gemini(query, full_context)
    return {"answer": response}
