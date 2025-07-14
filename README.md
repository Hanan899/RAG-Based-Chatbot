Here is your final **professional `README.md`** ready for uploading to GitHub for your OCR-based RAG Chatbot project:



# 🔍 OCR-Based RAG Chatbot using FastAPI, Streamlit & Gemini

This project is a document-based chatbot built using **OCR**, **vector similarity search**, and **LLMs (Gemini API)**. It enables users to upload scanned PDFs, extract content using OCR, store meaningful chunks in a vector store, and interact with the documents through natural language queries. A real-world example of **Retrieval-Augmented Generation (RAG)** in action.


## 🚀 Features

- 📄 Upload scanned PDFs (e.g., research papers, handwritten notes, textbooks)
- 🧠 OCR processing using Tesseract + OpenCV
- 📚 Semantic chunking and embedding generation using `sentence-transformers`
- 🔍 Vector search using ChromaDB (LangChain)
- 🤖 Gemini Pro (Generative AI) for natural language answer generation
- ⚡ FastAPI backend for processing and querying
- 🌐 Streamlit frontend for chat interaction

---

## 📁 Project Structure

```

OCR-RAG-Chatbot/
│
├── app.py                      # FastAPI backend (document ingestion & chat endpoint)
├── frontend.py                # Streamlit UI
├── chroma/                    # Vector store data (auto-generated)
├── data/                      # Uploaded PDFs
├── .venv/                     # Python virtual environment
└── utils/
├── document\_loader.py     # Handles OCR from PDF bytes
├── text\_splitter.py       # Splits documents into overlapping chunks
├── vector\_store.py        # VectorDB handling (store, load, search)
└── image\_preprocess.py    # Enhances scanned images before OCR

````

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ocr-rag-chatbot.git
cd ocr-rag-chatbot
````

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure your environment

Ensure these tools are installed:

* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and its path set in `document_loader.py`
* [Poppler](http://blog.alivate.com.au/poppler-windows/) for PDF to image conversion
* [Gemini API key](https://makersuite.google.com/app) exported as:

```bash
export GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the backend

```bash
uvicorn app:app --reload
```

### 5. Run the frontend

```bash
streamlit run frontend.py
```

---

## ✨ How It Works

1. **PDF Upload**: User uploads scanned PDF files through Streamlit.
2. **OCR Extraction**: Each page is preprocessed with OpenCV and passed to Tesseract.
3. **Chunking**: Text is split into overlapping chunks using LangChain.
4. **Embedding**: Chunks are embedded with HuggingFace's MiniLM model.
5. **Storage**: Embeddings are stored in Chroma vector DB.
6. **Querying**: When a user asks a question, relevant chunks are retrieved and passed to Gemini for generating an answer.

---

## 🧪 Example Use Cases

* Document Q\&A Assistant (SOPs, policies)
* University Note & Book Chatbot
* Legal Document Analyzer
* Research Assistant for PDFs

---

## ✅ Sample Query

> Upload: `Machine Learning.pdf`
> Ask: *"What are supervised learning types?"*
> Response: Gemini generates an answer using chunks related to supervised learning from your file.

---

## 📦 Dependencies

* `FastAPI`, `Uvicorn`
* `Streamlit`
* `LangChain`, `Chroma`
* `Tesseract`, `OpenCV`, `pdf2image`
* `HuggingFace sentence-transformers`
* `Google Generative AI SDK (Gemini)`

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute.

---

## 🙋‍♂️ Author

**Abdul Hanan**
AI Engineer | Robotics | ML Researcher
🔗 [LinkedIn Profile](https://www.linkedin.com/in/abdul-hanan-2003-)

---

## 💡 Want to Contribute?

Pull requests, suggestions, and issues are welcome!
If you'd like to expand this project (e.g., add RAG agents, online deployment, audio support), feel free to fork and contribute.



Let me know if you'd like a:

- `requirements.txt` file  
- `Dockerfile`  
- `Gemini Agent support`  
- `LangChain + OpenRouter` alternative version  
- or complete deployment instructions for Streamlit Cloud, Hugging Face Spaces, or Render.
