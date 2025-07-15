import requests
import os
import pyttsx3
from dotenv import load_dotenv

# 🗣️ Initialize TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 📨 Send plain text message to Telegram
def send_telegram(msg):
    bot_token = "7473219759:AAE672Tgap54wnQoTH2tZHWJQ0KV4eb-FBU"
    chat_id = "6097065132"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    try:
        response = requests.post(url, data=payload, timeout=10)
        print("\U0001F4E8 Telegram alert sent!")
        print("\U0001F4EC Telegram API response:", response.text)
    except Exception as e:
        print(f"\u274C Telegram error: {e}")

# 🔐 Load API key
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
LOCATION = "Bandipora"

# 🌦️ Weather API call
url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=3&alerts=yes&aqi=yes"

try:
    response = requests.get(url, timeout=30)
    data = response.json()

    location = data["location"]
    current = data["current"]

    # 📄 Build final report
    final_report = (
        "🔔 FINAL WEATHER REPORT\n\n"
        f"📍 Location: {location['name']}, {location['region']}, {location['country']}\n"
        f"🌡️ Temp: {current['temp_c']}\u00b0C\n"
        f"☁️ Condition: {current['condition']['text']}\n"
        f"🕒 Time: {'Day' if current['is_day'] else 'Night'}\n"
    )

    if any(w in current['condition']['text'].lower() for w in ["storm", "rain", "fog", "hail", "snow", "thunder"]):
        final_report += "\n⚠️ Alert: Risky weather right now!\n"

    # 🌤️ Forecast
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

    # 💧 Humidity & UV
    humidity = current["humidity"]
    uv_index = current["uv"]
    final_report += f"\n💧 Humidity: {humidity}%\n"
    final_report += f"🔆 UV Index: {uv_index}\n"

    # �� Air Quality (US EPA scale)
    if "air_quality" in current:
        aqi_us = current["air_quality"].get("us-epa-index")
        aqi_msg = {
            1: "Good",
            2: "Moderate",
            3: "Unhealthy for sensitive groups",
            4: "Unhealthy",
            5: "Very Unhealthy",
            6: "Hazardous"
        }.get(int(aqi_us), "Unknown")
        final_report += f"�� AQI (US): {aqi_us} - {aqi_msg}\n"

    # ✅ Print & Send
    print(final_report)
    send_telegram(final_report)

    # 🔊 Speak full weather summary
    summary_text = (
        f"Good {'morning' if current['is_day'] else 'evening'}! Here's the weather update for {location['name']}.\n"
        f"The temperature is {current['temp_c']} degrees Celsius with {current['condition']['text']}.\n"
        f"Humidity is around {humidity} percent and the UV index is {uv_index}.\n"
    )

    if any(w in current['condition']['text'].lower() for w in ["storm", "rain", "fog", "hail", "snow", "thunder"]):
        summary_text += "\u26a0️ Please be careful — risky weather conditions detected right now.\n"

    summary_text += "Here's your 3-day forecast:\n"
    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        cond = day["day"]["condition"]["text"]
        min_temp = day["day"]["mintemp_c"]
        max_temp = day["day"]["maxtemp_c"]

        summary_text += f"On {date}, expect {cond} with temperatures from {min_temp} to {max_temp} degrees.\n"

        if any(r in cond.lower() for r in ["storm", "thunder", "hail", "snow", "fog"]):
            summary_text += "⚠️ Be alert — this day may have severe weather.\n"

    if "air_quality" in current:
        summary_text += f"Air quality today is {aqi_msg} based on the US EPA scale.\n"

    speak(summary_text)

except requests.exceptions.RequestException as e:
    print(f"\u274C Weather API Error: {e}")
    speak("Weather API error. Please check your internet or API key.")
except Exception as e:
    print(f"\u274C Unexpected Error: {e}")
    speak("Something went wrong.")
