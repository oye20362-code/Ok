import os
import requests
from telegram.ext import Updater, CommandHandler
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def info(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Nhập username đi. Ví dụ:\n/info kien")
        return

    user = context.args[0]

    url = f"https://tiktok.livecounts.io/user/@{user}"
    data = requests.get(url).json()

    if "user" not in data:
        update.message.reply_text("Không tìm thấy user.")
        return

    user_data = data["user"]

    msg = f"""
📊 *Thông tin TikTok*  
👤 Username: @{user_data['uniqueId']}
🆔 ID: {user_data['id']}
📛 Tên: {user_data['nickname']}
👥 Follower: {user_data['followerCount']}
👤 Following: {user_data['followingCount']}
❤️ Tim: {user_data['heartCount']}
    """

    update.message.reply_text(msg, parse_mode="Markdown")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("info", info))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
