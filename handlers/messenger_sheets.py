import os
import requests
from flask import request
from dotenv import load_dotenv
from utils.gsheets_faq import find_answer  # ✅ Modular import

# Load environment variables
load_dotenv()

# Environment variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


# === Webhook Entry Point ===
def handle(request):
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        data = request.get_json()
        print("[DEBUG] Incoming webhook payload:", data)

        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for event in entry.get("messaging", []):
                    sender_id = event["sender"]["id"]

                    if "message" in event and "text" in event["message"]:
                        user_input = event["message"]["text"]
                        print(f"[DEBUG] Received message from user: '{user_input}'")

                        reply = find_answer(user_input)
                        send_message(sender_id, reply)

        return "ok", 200


# === Webhook Verification ===
def verify_webhook(request):
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"[DEBUG] Verifying webhook: mode={mode}, token={token}, expected={VERIFY_TOKEN}")

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


# === Send Reply to Messenger ===
def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    print(f"[DEBUG] Sending message to {recipient_id}: '{message_text}'")

    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        print(f"[ERROR] Failed to send message: {response.status_code} - {response.text}")
