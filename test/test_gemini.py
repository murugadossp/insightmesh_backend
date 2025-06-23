import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load the API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate API key
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it in your .env file.")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

if __name__ == "__main__":
    print(f"[LLM] Using API key: {GOOGLE_API_KEY[:6]}... (loaded)")

    # --- STEP 1: List all available models and their capabilities ---
    print("\n--- Available Gemini Models and their capabilities ---")
    available_models_for_text = []
    
    try:
        for m in genai.list_models():
            # Only consider models that support generating content (text, not just embeddings)
            if "generateContent" in m.supported_generation_methods and \
               "Move to a newer Gemini version" not in m.description:
                print(f"- Model Name: {m.name}")
                print(f"  Description: {m.description}")
                print(f"  Input Tokens: {m.input_token_limit}")
                print(f"  Output Tokens: {m.output_token_limit}")
                print(f"  Supported Methods: {m.supported_generation_methods}")
                print("-" * 30) # Separator for readability
                available_models_for_text.append(m.name)
            else:
                # Optionally print models that don't support generateContent, for full transparency
                # print(f"- Model Name: {m.name} (Does NOT support generateContent)")
                pass # Skipping models not relevant for this task

    except Exception as e:
        print(f"Error listing models: {e}")
        print("Please ensure your API key is correct and has access to the Generative Language API.")
        exit() # Exit if we can't even list models

    print("\n--- Summary of Available Gemini Models ---")
    print(f"Total models available for text generation: {len(available_models_for_text)}")
    print(f"Available models : \n {available_models_for_text} ")
    print("\n--- End of Available Models ---")


    
    # --- STEP 2: Attempt to use a suitable model ---
    model_to_use = None

    # Prioritize commonly used text models for hackathons, favoring cost-effectiveness (Flash, Lite, Gemma)
    # followed by higher-tier models if needed.
    priority_models = [
        "models/gemini-2.5-flash",           # Latest 2.5 Flash version
        "models/gemini-2.5-flash-lite",      # Even more cost-optimized for Flash family
        "models/gemini-2.0-flash",           # Stable, good balance of cost/performance
        "models/gemini-2.0-flash-lite",      # Even more cost-optimized for Flash family
        "models/gemma-3-1b-it",              # Highly cost-optimized, smaller model
        "models/gemini-2.5-pro",             # Latest 2.5 Pro version (highest cost)
        "models/gemini-pro"                  # Original gemini-pro (if it ever becomes available)
    ]

    for preferred_model in priority_models:
        if preferred_model in available_models_for_text:
            model_to_use = preferred_model
            break # Found a preferred model that is available

    if model_to_use:
        print(f"\n[LLM] Attempting to call model: {model_to_use}")
        try:
            model = genai.GenerativeModel(model_to_use)
            response = model.generate_content("Summarize this: Units Sold = 120, Revenue = 2400")
            print("\n--- Summary from LLM ---")
            print(response.text)
        except Exception as e:
            print(f"\n[LLM] Error calling {model_to_use}: {e}")
            print("Even though the model was listed, there might be a specific issue or quota limit.")
            print("Consider trying another model from the 'Available Gemini Models' list above.")
    else:
        print("\n--- No suitable text generation model found! ---")
        print("None of the common and recommended models were found to be available for `generateContent` with your API key.")
        print("Please review the 'Available Gemini Models' list above and manually select a model name.")
        print("You might need to check your Google Cloud project settings and region for API access or try generating a new API key.")

