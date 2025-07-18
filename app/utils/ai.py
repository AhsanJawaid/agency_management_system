import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_KEY"))

def proposal_generator(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating proposal: {str(e)}"
