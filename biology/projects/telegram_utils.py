import telegram
import logging

logger = logging.getLogger(__name__)

async def send_telegram_message(chat_id, message):
    bot_token = '7745917078:AAFxyoEh607mYeptZ4djKxES7SuvmPn9r6Y'
    bot = telegram.Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Повідомлення відправлено: {message}")
        print(f"Повідомлення відправлено: {message}")
    except telegram.error.TelegramError as e:
        logger.error(f"Помилка відправки повідомлення: {e}")
        print(f"Помилка відправки повідомлення: {e}")