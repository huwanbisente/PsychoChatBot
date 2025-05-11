import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

def generate_response(prompt):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    payload = {
        "inputs": prompt
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        result = response.json()
        return result.get("generated_text", "Sorry, I didn't understand that.")
    except Exception as e:
        return f"Error: {str(e)}"
