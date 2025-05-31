import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ВСТАВЬ СЮДА ТОКЕН ОТ BotFather
TELEGRAM_BOT_TOKEN = '7264583935:AAHtKlH3VedYl1EsLyn5_-Q5dtYUsMKWfFA'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Введите номер автомобиля (например, AA1234BC):")

def search_car_info(plate_number: str) -> str:
    plate_number = plate_number.strip().upper()

    results = []

    # --- UNDA.COM.UA ---
    try:
        url1 = f"http://www.unda.com.ua/gosnomer-UA/{plate_number}"
        r1 = requests.get(url1, timeout=10)
        soup1 = BeautifulSoup(r1.text, "html.parser")

        info1 = soup1.find("div", class_="entry-content")
        if info1:
            results.append(f"🔍 [UNDA]\n{info1.get_text(strip=True)}")
        else:
            results.append("🔍 [UNDA] - информация не найдена.")
    except Exception as e:
        results.append("🔍 [UNDA] - ошибка при получении данных.")

    # --- BAZA-GAI.COM.UA ---
    try:
        url2 = f"https://baza-gai.com.ua/nomer/{plate_number}"
        r2 = requests.get(url2, timeout=10)
        soup2 = BeautifulSoup(r2.text, "html.parser")

        main_info = soup2.find("div", class_="car-info")
        if main_info:
            results.append(f"🚓 [Baza-GAI]\n{main_info.get_text(strip=True)}")
        else:
            results.append("🚓 [Baza-GAI] - информация не найдена.")
    except Exception as e:
        results.append("🚓 [Baza-GAI] - ошибка при получении данных.")

    return "\n\n".join(results)

def handle_message(update: Update, context: CallbackContext):
    plate_number = update.message.text.strip().upper()
    update.message.reply_text(f"Ищу информацию для номера: {plate_number}...")
    result = search_car_info(plate_number)
    update.message.reply_text(result)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()