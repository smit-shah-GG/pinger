from flask import Flask, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import os
import atexit

app = Flask(__name__)

# Target URL is hardcoded for this specific use case
TARGET_URL = "https://tag-internlink-v2.onrender.com/api/health"
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", 60))  # defaults to 60 seconds


def ping_target():
    try:
        response = requests.get(TARGET_URL)
        print(f"Pinged {TARGET_URL} - Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Ping failed: {e}")


# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=ping_target, trigger="interval", seconds=PING_INTERVAL)
scheduler.start()

# Shut down scheduler when exiting
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def home():
    return jsonify(
        {
            "status": "Pinger is running",
            "target": TARGET_URL,
            "ping_interval": f"Every {PING_INTERVAL} seconds",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
