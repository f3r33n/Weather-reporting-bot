import requests

def send_telegram(msg):
    bot_token = "7473219759:AAE672Tgap54wnQoTH2tZHWJQ0KV4eb-FBU"
    chat_id = "6097065132"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    response = requests.post(url, data=payload)
    
    # Print the response to debug
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

# Test the bot
send_telegram("✅ Telegram bot is working! 🚀")
