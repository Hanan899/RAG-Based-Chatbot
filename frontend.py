import streamlit as st
import requests
import time
from datetime import datetime

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG ChatBot", layout="centered")
st.markdown("""
    <style>
        body { background-color: #f9f9f9; }
        .stChatMessage { border-radius: 12px; padding: 12px; margin-bottom: 10px; }
        .user-msg { background-color: #d1e7dd; color: #000; }
        .assistant-msg { background-color: #fff3cd; color: #000; }
        .css-10trblm { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>RAG ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>A Document-Aware Conversational System</h4>", unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat"):
        st.session_state.messages = []

    st.markdown("## Upload PDFs")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    if st.button("Process PDFs") and uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing: {uploaded_file.name}"):
                uploaded_file.seek(0)
                pdf_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
                res = requests.post(f"{FASTAPI_URL}/upload/", files=files)

            if res.status_code == 200:
                st.success(f"{uploaded_file.name} processed successfully!")
            else:
                st.error(f"Failed to process {uploaded_file.name}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"🧠 Tokens: `{msg.get('tokens', 'N/A')}` | ⏱️ Latency: `{msg.get('latency', 'N/A')}` sec")
            source = msg.get("source", None)
            if source:
                if source.startswith("PDF:"):
                    st.markdown("**📄 Sources from Documents:**")
                    for ref in source.replace("PDF:", "").split(" | "):
                        st.markdown(f"- `{ref.strip()}`")
                elif source.startswith("WEB:"):
                    st.markdown("**🌐 Source from the Web:**")
                    st.markdown(f"- {source.replace('WEB:', '').strip()}")
                else:
                    st.info(f"Source:\n{source}")

if prompt := st.chat_input("Ask a question..."):
    timestamp = datetime.now().strftime("%b %d, %I:%M %p")
    st.session_state.messages.append({"role": "user", "content": f"**You** ({timestamp})\n\n{prompt}"})

    with st.chat_message("user"):
        st.markdown(f"**You** ({timestamp})\n\n{prompt}")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{FASTAPI_URL}/chat/", params={"query": prompt})
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "No answer.")
                    tokens = data.get("tokens", "N/A")
                    source = data.get("source", "No source provided.")
                    latency = data.get("latency", None) or "N/A"
                else:
                    answer, tokens, latency, source = f"❌ Error: {res.text}", 0, "N/A", None
            except Exception as e:
                answer, tokens, latency, source = f"❌ Exception: {e}", 0, "N/A", None

            # --- Typing animation ---
            container = st.empty()
            typed = ""
            for char in answer:
                typed += char
                container.markdown(f"**Bot** ({timestamp})\n\n{typed}")
                time.sleep(0.01)

            st.caption(f"🧠 Tokens: `{tokens}` | ⏱️ Latency: `{latency}` sec")

            if source:
                if source.startswith("PDF:"):
                    st.markdown("**📄 Sources from Documents:**")
                    for ref in source.replace("PDF:", "").split(" | "):
                        st.markdown(f"- `{ref.strip()}`")
                elif source.startswith("WEB:"):
                    st.markdown("**🌐 Source from the Web:**")
                    st.markdown(f"- {source.replace('WEB:', '').strip()}")
                else:
                    st.info(f"Source:\n{source}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**Bot** ({timestamp})\n\n{answer}",
                "tokens": tokens,
                "latency": latency,
                "source": source
            })
