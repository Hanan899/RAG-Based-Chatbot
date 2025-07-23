from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(extracted_lines):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )

    chunks = []
    for line in extracted_lines:
        docs = text_splitter.create_documents([line["text"]], metadatas=[line["metadata"]])
        chunks.extend(docs)

    return chunks
