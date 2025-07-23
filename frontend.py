import streamlit as st
import requests
import time

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG ChatBot", layout="wide")
st.title("RAG ChatBot")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: File Upload Section ---
with st.sidebar:
    st.header("Upload PDFs")
    uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)

    if st.button("Process PDFs") and uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing: {uploaded_file.name}"):
                pdf_bytes = uploaded_file.read()
                files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
                res = requests.post(f"{FASTAPI_URL}/upload/", files=files)

            if res.status_code == 200:
                st.success(f"{uploaded_file.name} processed!")
            else:
                st.error(f"Failed to process {uploaded_file.name}")

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"🧠 Tokens: `{msg['tokens']}` | ⏱️ Latency: `{msg['latency']}` sec")
            if "source" in msg:
                source = msg["source"]
                if source.startswith("PDF:"):
                    formatted = source.replace("PDF:", "").strip()
                    references = formatted.split(" | ")
                    st.markdown("**📚 Sources from Documents:**")
                    for ref in references:
                        st.markdown(f"- `{ref.strip()}`")
                elif source.startswith("WEB:"):
                    st.markdown("**🌐 Source from the Web:**")
                    st.markdown(f"- {source.replace('WEB:', '').strip()}")
                else:
                    st.info(f"📚 Source:\n{source}")

# --- Chat Input Box ---
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start = time.time()
            try:
                res = requests.post(f"{FASTAPI_URL}/chat/", params={"query": prompt})
                end = time.time()

                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "No answer.")
                    
                    # Replace fallback answers
                    if "I do not have access" in answer or "I’m sorry" in answer or "I am sorry" in answer:
                        answer = "I'm sorry"

                    tokens = data.get("tokens", "N/A")
                    latency = round(end - start, 2)
                    source = data.get("source", "📚 No source provided.")

                    st.markdown(answer)
                    st.caption(f"🧠 Tokens: `{tokens}` | ⏱️ Latency: `{latency}` sec")

                    if source.startswith("PDF:"):
                        formatted = source.replace("PDF:", "").strip()
                        references = formatted.split(" | ")
                        st.markdown("**📚 Sources from Documents:**")
                        for ref in references:
                            st.markdown(f"- `{ref.strip()}`")
                    elif source.startswith("WEB:"):
                        st.markdown("**🌐 Source from the Web:**")
                        st.markdown(f"- {source.replace('WEB:', '').strip()}")
                    else:
                        st.info(f"📚 Source:\n{source}")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "tokens": tokens,
                        "latency": latency,
                        "source": source
                    })

                else:
                    error_msg = f"❌ Error: {res.text}"
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
