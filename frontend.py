import streamlit as st
import requests
import time
from datetime import datetime

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG ChatBot", layout="wide")
st.markdown("<h1 style='text-align: center;'>RAG ChatBot Assistant</h1>", unsafe_allow_html=True)

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: File Upload Section ---
with st.sidebar:
    st.markdown("## Upload PDFs")
    uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)

    if st.button("Process PDFs") and uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing: {uploaded_file.name} ({round(len(uploaded_file.read())/1024, 2)} KB)"):
                uploaded_file.seek(0)  # Reset file pointer
                pdf_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
                res = requests.post(f"{FASTAPI_URL}/upload/", files=files)

            if res.status_code == 200:
                st.success(f" {uploaded_file.name} processed successfully!")
            else:
                st.error(f" Failed to process {uploaded_file.name}")

# --- Display Chat History ---
for msg in st.session_state.messages:
    role = msg["role"]
    timestamp = msg.get("timestamp", "")
    content = msg["content"]
    tokens = msg.get("tokens", "N/A")
    latency = msg.get("latency", "N/A")
    source = msg.get("source", None)

    with st.chat_message(role):
        st.markdown(f"**{'Hanan' if role=='user' else 'Agent'}** ({timestamp})", unsafe_allow_html=True)
        st.markdown(f"> {content}")
        if role == "agent":
            st.caption(f"🧠 Tokens: `{tokens}` | ⏱️ Latency: `{latency}` sec")

            if source:
                if source.startswith("PDF:"):
                    st.markdown("**Sources from Documents:**")
                    for ref in source.replace("PDF:", "").split(" | "):
                        st.markdown(f"- `{ref.strip()}`")
                elif source.startswith("WEB:"):
                    st.markdown("**Source from the Web:**")
                    st.markdown(f"- {source.replace('WEB:', '').strip()}")
                else:
                    st.info(f"Source:\n{source}")

# --- Chat Input Box ---
if prompt := st.chat_input("Ask a question..."):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    with st.chat_message("user"):
        st.markdown(f"**Hanan** ({timestamp})")
        st.markdown(f"> {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("Agent Thinking..."):
            start = time.time()
            try:
                res = requests.post(f"{FASTAPI_URL}/chat/", params={"query": prompt})
                end = time.time()

                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "No answer.")
                    if any(phrase in answer for phrase in ["I do not have access", "I’m sorry", "I am sorry"]):
                        answer = "I'm sorry"

                    tokens = data.get("tokens", "N/A")
                    latency = round(end - start, 2)
                    source = data.get("source", "No source provided.")

                    # Typing effect simulation
                    container = st.empty()
                    typed = ""
                    for char in answer:
                        typed += char
                        container.markdown(f"**Agent ({timestamp})**\n\n> {typed}")
                        time.sleep(0.01)

                    st.caption(f"🧠 Tokens: `{tokens}` | ⏱️ Latency: `{latency}` sec")
                    if source.startswith("PDF:"):
                        st.markdown("**Sources from Documents:**")
                        for ref in source.replace("PDF:", "").split(" | "):
                            st.markdown(f"- `{ref.strip()}`")
                    elif source.startswith("WEB:"):
                        st.markdown("**Source from the Web:**")
                        st.markdown(f"- {source.replace('WEB:', '').strip()}")
                    else:
                        st.info(f"Source:\n{source}")

                    st.session_state.messages.append({
                        "role": "agent",
                        "content": answer,
                        "tokens": tokens,
                        "latency": latency,
                        "timestamp": timestamp,
                        "source": source
                    })

                else:
                    error_msg = f"❌ Error: {res.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "agent",
                        "content": error_msg,
                        "tokens": 0,
                        "latency": 0,
                        "timestamp": timestamp
                    })

            except Exception as e:
                error_msg = f"❌ Exception: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "agent",
                    "content": error_msg,
                    "tokens": 0,
                    "latency": 0,
                    "timestamp": timestamp
                })
