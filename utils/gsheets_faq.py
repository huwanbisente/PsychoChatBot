import os
import json
import gspread
from dotenv import load_dotenv
from difflib import get_close_matches
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "ChatBotFAQ")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDS")

def get_gsheet_client():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def load_faq_from_sheet():
    try:
        client = get_gsheet_client()
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
    faq = load_faq_from_sheet()
    user_input = user_input.strip().lower()

    print(f"[DEBUG] Looking for answer to: '{user_input}'")
    matches = get_close_matches(user_input, faq.keys(), n=1, cutoff=0.6)

    if matches:
        matched_question = matches[0]
        print(f"[DEBUG] Fuzzy match found: '{matched_question}'")
        return faq[matched_question]

    print(f"[DEBUG] No match found for: '{user_input}'")
    return None

def get_all_questions(limit=5):
    try:
        client = get_gsheet_client()
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        records = sheet.get_all_records()
        questions = [row["Question"].strip() for row in records if "Question" in row]
        return questions[:limit]
    except Exception as e:
        print(f"[ERROR] Failed to load questions: {e}")
        return []
