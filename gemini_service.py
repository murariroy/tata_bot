

import os
from dotenv import load_dotenv
from langchain_google_vertexai import VertexAI
from google_custom_search import search_google_custom

load_dotenv()

def ask_gemini(question: str, context: list) -> str:
    """Query Gemini with context and optional search results for better responses."""
    try:
       
        with open("prompt.txt", "r", encoding="utf-8") as file:
            base_prompt = file.read().strip()

       
        gcs_info = search_google_custom(question)
        gcs_info = gcs_info if gcs_info else "No verified references found."
     
       

        history = ""
        for pair in context:
            history += f"User: {pair['user']}\nAssistant: {pair['ai']}\n"

        
        full_prompt = f"""
{base_prompt}

## Context:
{history}

## User Query:
"{question}"

## Google Reference:
{gcs_info}

## Guidelines:
- Provide a precise, professional, and easy-to-understand explanation.
- Use the Google reference above to inform your reply.
- Do not mention Google or external search engines.
- Do not include URLs unless part of the reference.
- Avoid marketing phrases; focus on facts.
"""

        
        model = VertexAI(model_name="gemini-1.5-pro")
        gemini_answer = model.invoke(full_prompt).strip()

        return gemini_answer

    except Exception as e:
        return f"Gemini error: {str(e)}"
