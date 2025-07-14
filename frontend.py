import streamlit as st
import requests
import time

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("RAG Chatbot")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ocr_preview" not in st.session_state:
    st.session_state.ocr_preview = []

# --- SIDEBAR: File Upload Section ---
with st.sidebar:
    st.header("📎 Upload PDFs")
    uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)

    if st.button("📤 Process PDFs") and uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing: {uploaded_file.name}"):
                pdf_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
                res = requests.post(f"{FASTAPI_URL}/upload/", files=files)

            if res.status_code == 200:
                st.success(f"{uploaded_file.name} processed!")
                preview_text = f"OCR preview: {uploaded_file.name}\n\n..."
                st.session_state.ocr_preview.append((uploaded_file.name, preview_text))
            else:
                st.error(f"Failed to process {uploaded_file.name}")

    # OCR Preview
    if st.session_state.ocr_preview:
        st.markdown("---")
        st.subheader("🖼️ OCR Previews")
        for name, preview in st.session_state.ocr_preview:
            with st.expander(name):
                st.text(preview[:1000] + "...")



# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"🧠 Tokens: `{msg['tokens']}` | ⏱️ Latency: `{msg['latency']}`")

# Chat input field
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start = time.time()
            try:
                response = requests.post(f"{FASTAPI_URL}/chat/", params={"query": prompt})
                end = time.time()

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    tokens = data.get("tokens", "N/A")
                    latency = round(end - start, 2)

                    st.markdown(answer)
                    st.caption(f"🧠 Tokens: `{tokens}` | ⏱️ Latency: `{latency}` sec")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "tokens": tokens,
                        "latency": latency
                    })
                else:
                    error_msg = f"❌ Error: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "tokens": 0,
                        "latency": 0
                    })

            except Exception as e:
                error_msg = f"❌ Exception: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "tokens": 0,
                    "latency": 0
                })
