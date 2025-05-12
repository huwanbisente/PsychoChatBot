import os
import requests
from flask import request
from dotenv import load_dotenv
from utils.gsheets_faq import find_answer, get_all_questions

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

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

                        if user_input.lower() in ["help", "menu", "options"]:
                            questions = get_all_questions()
                            quick_replies = [
                                {
                                    "content_type": "text",
                                    "title": q[:20],
                                    "payload": q.lower().replace(" ", "_")
                                }
                                for q in questions
                            ]

                            send_quick_replies(sender_id, {
                                "text": "Here are some questions you can ask:",
                                "quick_replies": quick_replies
                            })
                        else:
                            reply = find_answer(user_input)
                            if reply:
                                send_message(sender_id, reply)
                            else:
                                questions = get_all_questions()
                                quick_replies = [
                                    {
                                        "content_type": "text",
                                        "title": q[:20],
                                        "payload": q.lower().replace(" ", "_")
                                    }
                                    for q in questions
                                ]

                                send_quick_replies(sender_id, {
                                    "text": "Sorry, I couldn't find an answer for that. Try one of these:",
                                    "quick_replies": quick_replies
                                })

        return "ok", 200

def verify_webhook(request):
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"[DEBUG] Verifying webhook: mode={mode}, token={token}, expected={VERIFY_TOKEN}")

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = { "Content-Type": "application/json" }
    params = { "access_token": PAGE_ACCESS_TOKEN }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    print(f"[DEBUG] Sending message to {recipient_id}: '{message_text}'")
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        print(f"[ERROR] Failed to send message: {response.status_code} - {response.text}")

def send_quick_replies(recipient_id, message_payload):
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = { "Content-Type": "application/json" }
    params = { "access_token": PAGE_ACCESS_TOKEN }
    payload = {
        "recipient": {"id": recipient_id},
        "message": message_payload
    }

    print(f"[DEBUG] Sending quick replies to {recipient_id}: {payload}")
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        print(f"[ERROR] Failed to send quick replies: {response.status_code} - {response.text}")
