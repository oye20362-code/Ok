import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from TikTokApi import TikTokApi

api = TikTokApi()

# ===== COMMAND: /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot TikTok Online ✔\nGửi /info username")

# ===== COMMAND: /info username =====
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("Nhập username: /info therock")

    username = context.args[0].replace("@", "")

    try:
        user = api.user(username=username)
        data = await user.info()

        user_info = data["userInfo"]["user"]

        text = (
            f"📊 *THÔNG TIN TIKTOK*\n"
            f"• Username: @{user_info['uniqueId']}\n"
            f"• ID: {user_info['id']}\n"
            f"• secUid: {user_info['secUid']}\n"
            f"• Tên hiển thị: {user_info.get('nickname','N/A')}\n"
            f"• Follower: {user_info['stats']['followerCount']}\n"
            f"• Following: {user_info['stats']['followingCount']}\n"
            f"• Video: {user_info['stats']['videoCount']}\n"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Lỗi không lấy được info!\n{e}")

# ===== COMMAND: /videos username =====
async def videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("Nhập username: /videos therock")

    username = context.args[0].replace("@", "")
    msg = await update.message.reply_text("Đang lấy video...")

    try:
        user = api.user(username=username)
        gen = user.videos(count=5)

        async for v in gen:
            video_data = v.as_dict

            link = f"https://www.tiktok.com/@{username}/video/{video_data['id']}"
            await update.message.reply_text(link)

        await msg.edit_text("Hoàn tất ✔")

    except Exception as e:
        await msg.edit_text(f"Lỗi: {e}")

# ===== MAIN =====
async def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("videos", videos))

    print("Bot chạy rồi ✔")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
