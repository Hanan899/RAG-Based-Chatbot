import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

chat_groq = ChatGroq(model="openai/gpt-oss-120b",
                    api_key=os.getenv("GROQ_API_KEY"))

# Common phrases that indicate no useful answer
FALLBACK_PHRASES = [
    "i don't know",
    "i'm sorry",
    "not sure",
    "no information",
    "i could not find",
    "unable to find",
    "is not available",
]

def generate_answer_from_groq(query, context):

    if context:
        print(f"🔍 Context provided for query: {query}")
        print(f"🔍 Context length: {len(context)} characters")
        prompt = f"""
You are an expert assistant. Use the context below to answer the user's question.
If the answer is not in the context, just say you don't know.

Context:
\"\"\"{context}\"\"\"

Question: {query}
Answer:
        """
    else:
        print(f"🔍 No context provided for query: {query}")
        prompt = f"""
You are a general-purpose AI assistant. The user has asked a question.
Respond based on your own training and knowledge.

Question: {query}
Answer:
        """

    try:
        response = chat_groq.invoke(prompt)
        answer = response.content.strip() if hasattr(response, "content") else str(response).strip()
        print(f"🤖 Groq Answer: {answer[:500]}...")

        # Check for fallback triggers
        if any(phrase in answer.lower() for phrase in FALLBACK_PHRASES):
            print("⚠️ Groq returned an unhelpful answer. Triggering web search fallback.")
            return None  # Or some flag to indicate fallback
        return answer

    except Exception as e:
        print(f"❌ Error while generating response: {str(e)}")
        return f"❌ Error: {str(e)}"
