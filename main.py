import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ================== تنظیمات ==================
TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# ============================================

def get_tmdb_info(title):
    url = f"https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data.get('results'):
            return "❌ نتونستم فیلم/سریال رو پیدا کنم.\nاسم رو دقیق‌تر بنویس."
        
        item = data['results'][0]
        media_type = item.get('media_type', 'movie')
        
        # جزئیات کامل
        detail_url = f"https://api.themoviedb.org/3/{media_type}/{item['id']}"
        detail_resp = requests.get(detail_url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
        detail = detail_resp.json()
        
        name = detail.get('title') or detail.get('name', title)
        year = (detail.get('release_date') or detail.get('first_air_date') or '')[:4]
        overview = detail.get('overview', 'خلاصه موجود نیست.')
        rating = detail.get('vote_average', 0)
        genres = [g['name'] for g in detail.get('genres', [])][:4]
        
        tag = "#series" if media_type == "tv" else "#film"
        genre_tags = " ".join(["#" + g.replace(" ", "").replace("-", "") for g in genres]) if genres else ""
        
        output = f"""{name} ({year if year else '????'})
{overview}
{rating:.1f}/10
{tag}
{genre_tags}
"""
        return output.strip()
    except:
        return "❌ خطا در دریافت اطلاعات. دوباره امتحان کن."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text.lower() in ['/start', '/help']:
        await update.message.reply_text("🎥 اسم فیلم یا سریال رو بفرست، برات با فرمت مرتب آماده می‌کنم!")
        return
    
    await update.message.reply_text("🔍 در حال جستجو...")
    result = get_tmdb_info(text)
    await update.message.reply_text(result)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 ربات با موفقیت شروع شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
