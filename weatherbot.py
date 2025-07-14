import requests
import os
from dotenv import load_dotenv

# 📨 Send plain text message to Telegram
def send_telegram(msg):
    bot_token = "7473219759:AAE672Tgap54wnQoTH2tZHWJQ0KV4eb-FBU"
    chat_id = "6097065132"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        print("📨 Telegram alert sent!")
        print("📬 Telegram API response:", response.text)
    except Exception as e:
        print(f"❌ Telegram error: {e}")

# 🔐 Load API key
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
LOCATION = "Bandipora"

# 🌦️ Weather API
url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=3&alerts=yes"

try:
    response = requests.get(url, timeout=20)
    data = response.json()

    location = data["location"]
    current = data["current"]

    # 📄 Build plain text report
    final_report = (
        "🔔 FINAL WEATHER REPORT\n\n"
        f"📍 Location: {location['name']}, {location['region']}, {location['country']}\n"
        f"🌡️ Temp: {current['temp_c']}°C\n"
        f"☁️ Condition: {current['condition']['text']}\n"
        f"🕒 Time: {'Day' if current['is_day'] else 'Night'}\n"
    )

    if any(w in current['condition']['text'].lower() for w in ["storm", "rain", "fog", "hail", "snow", "thunder"]):
        final_report += "\n⚠️ Alert: Risky weather right now!\n"

    # 🌦️ 3-day forecast
    forecast_summary = "\n📅 3-Day Forecast:\n"
    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        cond = day["day"]["condition"]["text"]
        min_temp = day["day"]["mintemp_c"]
        max_temp = day["day"]["maxtemp_c"]

        forecast_summary += f"• {date} - {cond}, {min_temp}°C to {max_temp}°C\n"

        if any(w in cond.lower() for w in ["storm", "thunder", "hail", "snow", "fog"]):
            forecast_summary += "⚠️ Risky day!\n"

    final_report += forecast_summary

    # ✅ Send message to Telegram
    print(final_report)
    send_telegram(final_report)

except requests.exceptions.RequestException as e:
    print(f"❌ Weather API Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
