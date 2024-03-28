import threading
import time

from bot import bot
from autocon import download_convert_schedule

def run_bot():
    bot.infinity_polling(timeout=5, long_polling_timeout=10)


def run_schedule():
    while True:
        download_convert_schedule()
        time.sleep(600)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    schedule_thread = threading.Thread(target=run_schedule)

    bot_thread.start()
    schedule_thread.start()