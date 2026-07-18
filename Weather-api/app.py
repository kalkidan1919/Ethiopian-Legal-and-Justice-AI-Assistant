import json
import urllib.request
import urllib.error

def load_profile():
    """Loads the user profile from profile.json with safety fallbacks."""
    try:
        with open("profile.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ Error: 'profile.json' not found. Creating a temporary one.")
        return {"name": "Guest", "city": "Unknown", "latitude": 0.0, "longitude": 0.0}
    except json.JSONDecodeError:
        print("❌ Error: 'profile.json' has invalid formatting. Using default values.")
        return {"name": "Guest", "city": "Unknown", "latitude": 0.0, "longitude": 0.0}

def fetch_local_weather(lat, lon):
    """Fetches real-time weather from Open-Meteo API using standard library."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
    
    try:
        # 4-second timeout ensures our terminal doesn't freeze indefinitely
        with urllib.request.urlopen(url, timeout=4) as response:
            data = json.loads(response.read().decode())
            return data.get("current", {})
    except urllib.error.URLError as e:
        print(f"⚠️ Network warning: Could not load weather data ({e.reason}).")
        return None
    except Exception:
        print("⚠️ General warning: Weather API is currently unavailable.")
        return None

def main():
    profile = load_profile()
    
    # Header display
    print("=========================================")
    print(f"       DEVELOPER PROFILE: {profile.get('name', 'N/A').upper()}       ")
    print("=========================================")
    print(f"📍 Role:     {profile.get('role', 'N/A')}")
    print(f"🌍 Location: {profile.get('city', 'N/A')}")
    
    # Integrate live API data
    lat = profile.get("latitude")
    lon = profile.get("longitude")
    
    if lat is not None and lon is not None:
        print("\n⏳ Loading live environmental data...")
        weather = fetch_local_weather(lat, lon)
        
        if weather:
            temp = weather.get("temperature_2m", "N/A")
            humidity = weather.get("relative_humidity_2m", "N/A")
            print(f"☀️ Current Temp: {temp}°C")
            print(f"💧 Humidity:     {humidity}%")
        else:
            print("☀️ Live Weather: Weather data unavailable at the moment.")
    else:
        print("\n☀️ Live Weather: Location coordinates missing from profile.")
        
    print("=========================================")

if __name__ == "__main__":
    main()
