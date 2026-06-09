import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ================== CONFIG ==================
TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# ============================================


def get_tmdb_info(title):
    url = "https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()

        if "results" in data and len(data["results"]) > 0:
            item = data["results"][0]
            name = item.get("title") or item.get("name", "Unknown")
            overview = item.get("overview", "No description")
            return f"🎬 {name}\n\n{overview}"
        else:
            return "❌ چیزی پیدا نشد"

    except Exception as e:
        return f"⚠️ خطا: {str(e)}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = get_tmdb_info(text)
    await update.message.reply_text(result)


def main():
    if not TOKEN:
        print("BOT_TOKEN is missing!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
