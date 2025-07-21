import google.generativeai as genai
import os

genai.configure(api_key="Key")


FALLBACK_PHRASES = [
    "i don't know",
    "i'm sorry",
    "not sure",
    "no information",
    "i could not find",
    "unable to find",
    "is not available",
]

def generate_answer_from_gemini(query, context):
    model = genai.GenerativeModel("gemini-2.0-flash")

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
You are a general-purpose AI assistant with knowledge up to date till 2024. The user has asked a question.
Respond based on your own training and knowledge.

Question: {query}
Answer:
        """

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        print(f"🤖 Gemini Answer: {answer[:300]}...")

        # Check for fallback triggers
        if any(phrase in answer.lower() for phrase in FALLBACK_PHRASES):
            print("⚠️ Gemini returned an unhelpful answer. Triggering web search fallback.")
            return None  # Or some flag to indicate fallback
        return answer

    except Exception as e:
        print(f"❌ Error while generating response: {str(e)}")
        return f"❌ Error: {str(e)}"


    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error while generating response: {str(e)}"
