import os
from telegram.ext import Updater, CommandHandler
from flask import Flask

TOKEN = os.getenv("7945845706:AAGW_jEqxpaSuwsbnsg-RU7-rIPEt7MKr_g")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def start(update, context):
    update.message.reply_text("Bot Telegram hoạt động!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
