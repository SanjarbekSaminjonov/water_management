import datetime
import requests


def send_message_to_admin(message: str):
    BOT_TOKEN = "6189970014:AAHus7PaNaXmnBprScMqnRciirRNWUO7XV0"
    CHAT_ID = "-1002023472947"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    requests.post(url, data=data)


def get_formatted_time(now: datetime.datetime) -> str:
    return now.strftime("%H:%M:%S %d/%m/%Y")
