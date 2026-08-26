import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from scraper import CinemaBRScraper
from telegraph_upload import TelegraphUploader
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found")

scraper = CinemaBRScraper()
telegraph = TelegraphUploader()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🎬 **Bem-vindo ao Cinema BR Indie Bot!**

Eu sou seu assistente para o cinema independente brasileiro.

⚡ **Comandos:**
/festivais → Festivais em andamento
/submissoes → Prazos abertos
/noticias → Últimas notícias
/premiados → Filmes premiados
/hoje → Resumo diário com link Telegraph

Boa sorte com sua inscrição! 🍿
    """
    keyboard = [
        [InlineKeyboardButton("📅 Hoje", callback_data="today")],
        [InlineKeyboardButton("🎬 Festivais", callback_data="festivals")],
        [InlineKeyboardButton("📰 Notícias", callback_data="news")],
        [InlineKeyboardButton("🏅 Premiações", callback_data="awards")]
    ]
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def festivals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Buscando festivais...")
    data = scraper.get_festivals()
    if data:
        response = "🏆 **Festivais em Andamento:**\n\n"
        for f in data[:5]:
            response += f"🎬 **{f['name']}**\n📝 {f['description']}\n🔗 {f['link']}\n⏰ {f['deadline']}\n\n"
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Nenhum festival encontrado.")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Buscando notícias...")
    data = scraper.get_news()
    if data:
        response = "📰 **Últimas Notícias:**\n\n"
        for n in data[:5]:
            response += f"📌 **{n['title']}**\n📡 {n['source']}\n🔗 {n['link']}\n\n"
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Nenhuma notícia encontrada.")

async def awards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = scraper.get_awards()
    response = "🏅 **Premiações:**\n\n"
    for a in data:
        response += f"**{a['name']}**\n🏷️ {a['category']}\n🏆 {a['winner']}\n📅 {a['year']}\n\n"
    await update.message.reply_text(response, parse_mode='Markdown')

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Gerando resumo diário...")
    data = scraper.get_daily_summary()
    url = telegraph.create_daily_article(data)
    if url:
        response = f"""
📅 **Resumo do Cinema Independente BR** - {data['date']}

📊 {len(data['festivals'])} festivais | {len(data['news'])} notícias | {len(data['awards'])} premiações

📖 **Leia a análise completa:**
{url}
        """
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Erro ao gerar resumo.")

async def submissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = """
📅 **Prazos de Submissão Abertos:**

🎬 Festival de Gramado 2026
🔗 https://www.festivaldegramado.net

🎬 Mostra de Cinema de Tiradentes
🔗 https://www.mostratiradentes.com.br

🎬 Festival do Rio 2026
🔗 https://www.festivaldorio.com.br

📢 Editais ANCINE: https://www.gov.br/ancine
    """
    await update.message.reply_text(response, parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "today":
        await today(update, context)
    elif query.data == "festivals":
        await festivals(update, context)
    elif query.data == "news":
        await news(update, context)
    elif query.data == "awards":
        await awards(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("festivais", festivals))
    app.add_handler(CommandHandler("noticias", news))
    app.add_handler(CommandHandler("premiados", awards))
    app.add_handler(CommandHandler("hoje", today))
    app.add_handler(CommandHandler("submissoes", submissions))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🤖 Cinema BR Indie Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
