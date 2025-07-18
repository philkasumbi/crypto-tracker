import os
from datetime import datetime
import csv
import requests
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(filename):
    msg = EmailMessage()
    msg["Subject"] = "Crypto Data Report"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "kasumbipeter5@gmail.com"

    msg.set_content(f"Hi Philip,\n\nPlease find attached the crypto data: {filename}\n\n🚀 Keep tracking the market!")

    with open(filename, "rb") as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"📧 Email sent with {file_name}")

def crypto():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "crypto_data.csv"

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': False
    }

    response = requests.get(url, params=params)
    coins = response.json()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Symbol", "Price (USD)", "Market Cap", "24h Change (%)", "High 24h", "Low 24h", "Timestamp"])

        for coin in coins:
            writer.writerow([
                coin['name'],
                coin['symbol'].upper(),
                coin['current_price'],
                coin['market_cap'],
                coin['price_change_percentage_24h'],
                coin['high_24h'],
                coin['low_24h'],
                timestamp
            ])

    send_email(filename)


while True:
    crypto()
    print("✅ Data written and email sent. Waiting 24 hours...")
    time.sleep(86400)
