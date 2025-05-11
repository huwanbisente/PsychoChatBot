import os
import requests
from utils.hf_chat import generate_response

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

def handle(request):
    # Webhook verification (GET)
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    # Incoming messages (POST)
    if request.method == 'POST':
        data = request.get_json()

        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for event in entry.get("messaging", []):
                    sender_id = event["sender"]["id"]
                    if "message" in event:
                        user_input = event["message"].get("text", "")
                        if user_input:
                            reply = generate_response(user_input)
                            send_message(sender_id, reply)
        return "ok", 200

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

    requests.post(url, headers=headers, params=params, json=payload)
