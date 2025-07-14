from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )
    all_chunks = []
    for doc in documents:
        chunks = text_splitter.create_documents([doc["text"]], metadatas=[{"source": doc["name"]}])
        all_chunks.extend(chunks)
    return all_chunks
