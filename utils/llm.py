import google.generativeai as genai
import os

genai.configure(api_key="Key")


def generate_answer_from_gemini(query, context):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an expert assistant. Use the context below to answer the user's question.
If the answer is not in the context, just say you don't know.

Context:
\"\"\"
{context}
\"\"\"

Question: {query}
Answer:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error while generating response: {str(e)}"