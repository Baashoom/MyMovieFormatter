import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def get_tmdb_info(title):
    url = "https://api.themoviedb.org/3/search/multi"

    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    }

    print("=" * 50)
    print("SEARCH:", title)

    try:
        response = requests.get(url, params=params, timeout=15)

        print("STATUS CODE:", response.status_code)
        print("URL:", response.url)

        data = response.json()

        print("TMDB RESPONSE:")
        print(data)

        results = data.get("results", [])

        print("RESULT COUNT:", len(results))

        if not results:
            return "❌ چیزی پیدا نشد"

        item = results[0]

        name = item.get("title") or item.get("name") or "Unknown"
        media_type = item.get("media_type", "unknown")
        overview = item.get("overview", "No description")

        if not overview:
            overview = "No description"

        return (
            f"🎬 {name}\n"
            f"📺 Type: {media_type}\n\n"
            f"{overview}"
        )

    except Exception as e:
        print("ERROR:", str(e))
        return f"⚠️ خطا: {e}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        print("=" * 50)
        print("MESSAGE RECEIVED:", text)

        result = get_tmdb_info(text)

        print("BOT REPLY:")
        print(result)

        await update.message.reply_text(result)

    except Exception as e:
        print("HANDLER ERROR:", str(e))
        await update.message.reply_text(f"⚠️ خطا: {e}")


def main():
    print("Starting bot...")

    print("BOT_TOKEN exists:", bool(TOKEN))
    print("TMDB_API_KEY exists:", bool(TMDB_API_KEY))

    if not TOKEN:
        raise ValueError("BOT_TOKEN not found")

    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
