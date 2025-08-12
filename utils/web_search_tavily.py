from tavily import TavilyClient
import re
from utils.llm import generate_answer_from_groq  # import your Groq LLM function

TAVILY_API_KEY = "Api_Key"
client = TavilyClient(api_key=TAVILY_API_KEY)

def clean_text(text):
    text = re.sub(r'[⃗π✓→←⇒≠≤≥°ﬁ]', '', text)
    text = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\$.*?\$', '', text)
    text = re.sub(r'\\[a-zA-Z]+\{(.*?)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'([a-z]{10,})', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'[\n\r\t]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\(\s*\)|\[\s*\]|\{\s*\}', '', text)
    return text.strip()

def web_search_structured_answer(query, max_results=3):
    try:
        # Step 1: Web Search
        response = client.search(query=query, search_depth="advanced", max_results=max_results)
        results = response.get("results", [])
        snippets = [res.get("content", "") for res in results if "content" in res]

        # Step 2: Clean combined snippets
        combined_raw_text = "\n\n".join(snippets)
        cleaned_context = clean_text(combined_raw_text)

        # Step 3: Call Gemini model
        structured_answer = generate_answer_from_groq(query, cleaned_context)

        return structured_answer

    except Exception as e:
        return f"❌ Search or processing error: {str(e)}"


    except Exception as e:
        return f"❌ Search or processing error: {str(e)}"

