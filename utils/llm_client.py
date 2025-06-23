import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key and model name from env or fallback defaults
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL_NAME = os.getenv("GOOGLE_MODEL_NAME", "models/gemini-2.5-flash")

# Validate API key
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it in your .env file.")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def summarize_with_llm(stats_text: str) -> str:
    try:
        # Debug info
        print(f"[LLM] Using model: {GOOGLE_MODEL_NAME}")
        print(f"[LLM] API Key Prefix: {GOOGLE_API_KEY[:6]}...")

        model = genai.GenerativeModel(GOOGLE_MODEL_NAME)

        # Prompt structure
        prompt = (
            "You are a smart business analyst. Given the following Pandas-style statistical summary of a dataset, "
            "write a clear, natural-language summary of the key insights:\n\n"
            f"{stats_text}"
        )

        response = model.generate_content(prompt)
        print("[LLM] Generation successful.")

        return response.text.strip()

    except Exception as e:
        print(f"[LLM ERROR] {type(e).__name__}: {e}")
        return f"(LLM unavailable) Key data statistics:\n{stats_text}"