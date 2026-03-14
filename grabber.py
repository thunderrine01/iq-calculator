from flask import Flask, request
import requests

app = Flask(__name__)

WEBHOOK = "https://discord.com/api/webhooks/1482323306198601780/bvnAqpLHXijSAMi0fwJQV-IZG2nXdoScT4MFttVL3e42cXtol1HiGDGqR1AdsscKDzKG"

@app.route("/")
def home():
    ip = request.remote_addr

    data = {
        "content": f"🌐 New visitor on website\nIP: {ip}"
    }

    requests.post(WEBHOOK, json=data)

    return f"Welcome! Your IP is {ip}"

app.run(host="0.0.0.0", port=5000)