import os
import gspread
import json
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

# Load config from environment
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "ChatBotFAQ")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDS")  # ✅ Load from env var

def load_faq_from_sheet():
    """Loads the FAQ from a Google Sheet into a dictionary."""
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        # ✅ Load service account credentials from JSON string
        creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        records = sheet.get_all_records()

        faq_dict = {}
        for row in records:
            question = row['Question'].strip().lower()
            answer = row['Answer'].strip()
            faq_dict[question] = answer

        print(f"[DEBUG] Loaded {len(faq_dict)} FAQs from Google Sheet.")
        return faq_dict

    except Exception as e:
        print(f"[ERROR] Failed to load Google Sheet: {e}")
        return {}

def find_answer(user_input):
    """Finds the best answer for a user's message."""
    faq = load_faq_from_sheet()
    user_input = user_input.strip().lower()

    print(f"[DEBUG] Looking for answer to: '{user_input}'")

    if user_input in faq:
        print(f"[DEBUG] Match found for: '{user_input}'")
        return faq[user_input]

    print(f"[DEBUG] No match found for: '{user_input}'")
    return "Sorry, I couldn't find an answer for that. Please try asking something else."
