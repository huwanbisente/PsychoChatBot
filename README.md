# 🤖 Messenger FAQ Chatbot (Google Sheets-Driven)

A Python-based Messenger chatbot that responds to user messages using answers stored in a connected Google Sheet. Built with Flask, gspread, and the Messenger Platform API. Designed for extensibility, modularity, and multi-page support.

---

## 📌 Features

- ✅ Auto-replies to user messages using a structured FAQ
- ✅ Google Sheet integration as a live knowledge base
- ✅ Easily extendable to support OpenAI or fallback AI
- ✅ Can be deployed to multiple Facebook Pages
- ✅ Built for local testing and cloud deployment (e.g., Render)

---

## ⚙️ Tech Stack

- Python (Flask)
- Facebook Messenger Platform API
- Google Sheets API (`gspread`, `oauth2client`)
- ngrok (for local tunneling)
- dotenv (for secure environment configs)

---

## 📁 Folder Structure

project-root/
├── app.py # Flask entry point
├── .env # Environment configuration
├── requirements.txt # Python dependencies
├── handlers/
│ └── messenger_sheets.py # Webhook + Messenger logic
├── utils/
│ └── gsheets_faq.py # Google Sheets integration
├── credentials.json # Google service account key (DO NOT COMMIT)


2. Add .env file:
ini
Copy
Edit
APP_ENV=local
VERIFY_TOKEN=your_verify_token
PAGE_ACCESS_TOKEN=your_page_access_token
GOOGLE_SHEET_NAME=ChatBotFAQ
GOOGLE_CREDENTIALS_FILE=credentials.json
⚠️ Share your Google Sheet with your service account email from credentials.json.

3. Run Flask + ngrok:
bash
Copy
Edit
python app.py
ngrok http 5000
Use your ngrok URL in Facebook Developer → Messenger → Webhook → Callback URL.

