from flask import Flask, request
from handlers import messenger_sheets as messenger  # ✅ Ensure filename matches your handler script

app = Flask(__name__)

@app.route('/webhook/messenger', methods=['GET', 'POST'])
def webhook_messenger():
    return messenger.handle(request)

@app.route('/', methods=['GET'])
def index():
    return "✅ Messenger chatbot webhook is running!", 200

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    env = os.getenv("APP_ENV", "local")

    if env == "production":
        from waitress import serve
        print("🚀 Running in production mode...")
        serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    else:
        print("⚙️ Running in local debug mode...")
        app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
