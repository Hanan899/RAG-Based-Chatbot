
# RAG Chatbot using FastAPI & Gemini

A smart document-based chatbot built with **Tesseract OCR**, **vector search (ChromaDB)**, and **LLMs (Groq)**. This app allows users to upload scanned PDFs, extract and embed content using OCR, store it in a vector store, store its references, and ask natural language questions. If no relevant answer is found in the PDFs, it falls back to **real-time web search using Tavily API**.

A practical example of **Retrieval-Augmented Generation (RAG)** with dynamic fallback.

---

## Architecture:

- Upload Base64 encoded PDF's 
- Extract text using Tesseract OCR
- Chunk & Embedded text with Hugging Face Transformers
- Semantic similarity search using ChromaDB
- Answer generation using Groq LLM
- Web fallback using Tavily API (when PDFs don't help)
- Interactive frontend with Streamlit
- FastAPI backend for modular logic

---

## 📁 Project Structure

```text
ocr-rag-chatbot/
│
├── app.py                  # FastAPI backend
├── frontend.py             # Streamlit interface
├── chroma/                 # Vector store (ChromaDB)
└── utils/
    ├── document_loader.py        # OCR with Tesseract
    ├── image_preprocess.py       # Preprocessing
    ├── text_splitter.py          # Chunking and references
    ├── vector_store.py           # Embeddings, ChromaDB and Vector similarity search
    ├── llm.py                    # LLM query answering
    └── web_search_tavily.py      # Tavily-based fallback logic
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Hanan899/RAG-Based-Chatbot.git
cd RAG-Based-Chatbot
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate     # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install required tools

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (add to PATH)
- [Poppler](http://blog.alivate.com.au/poppler-windows/) (for `pdf2image`)

```bash
export GROQ_API_KEY=your_api_key_here
```

- [Tavily API key](https://docs.tavily.com/) → export as:

```bash
export TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Run the backend (FastAPI)

```bash
uvicorn app:app --reload
```

### 5. Run the frontend (Streamlit)

```bash
streamlit run frontend.py
```

---

## How It Works

1. **User Uploads Base64 Encoded PDF** Decode to original → Converted to images → OCR via Tesseract  
2. **Text Chunked** into overlapping segments  
3. **Embeddings** generated using `sentence-transformers`  
4. **Stored in ChromaDB** for semantic search  
5. **Query Received** → Search vector store for matches  
6. If match:
   - Groq LLM uses PDF context  
7. If no match or vague response:
   - Tavily API retrieves web content → Answer via Groq

---

## Example Use Cases

- Internal PDF Q&A (manuals, policies)
- Academic Assistant (notes, research papers)
- Legal Document Interrogation
- Government Policy Bot
- Resume or Report Chatbot

---

## Sample Query

> Upload: `machine_learning_guide.pdf`  
> Ask: “What are model evaluation metrics?”  
> ✅ Groq replies based on PDF  
> ❌ If not found → Tavily gets Wikipedia content → Gemini replies

---

## Key Dependencies

- `fastapi`, `uvicorn`
- `streamlit`
- `sentence-transformers`
- `chromadb`
- `tesserocr`, `opencv-python`, `pdf2image`
- `langchain-groq` (Groq API)
- `tavily-python`

---

## Author

**Abdul Hanan**  
AI Intern @ Hazen Technologies  
[LinkedIn](https://www.linkedin.com/in/abdul-hanan-2003-)  
a.hananwork4@gmail.com

---

## Want to Contribute?

Contributions and forks are welcome!  
If you'd like to extend this chatbot with:
- Agent support
- Audio Input/Output
- Docker deployment
- Streamlit Cloud integration

Feel free to fork or open a pull request.
