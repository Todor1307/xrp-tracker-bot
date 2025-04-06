import requests
import time
import datetime
from flask import Flask

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = -1001234567890  # Replace with your actual channel ID

app = Flask(__name__)

@app.route("/")
def home():
    return "XRP Tracker Bot is running!"

def get_xrp_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"
    response = requests.get(url)
    return response.json()["ripple"]["usd"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def xrp_loop():
    print("✅ XRP Tracker started...")
    while True:
        try:
            price = get_xrp_price()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"📈 XRP цена: ${price}\n🕒 Време: {timestamp}"
            send_telegram_message(message)
            print(f"[{timestamp}] Испратено: XRP ${price}")
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(600)

if __name__ == "__main__":
    import threading
    threading.Thread(target=xrp_loop).start()
    app.run(host="0.0.0.0", port=8080)
