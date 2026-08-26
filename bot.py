import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from scraper import CinemaBRScraper
from telegraph_upload import TelegraphUploader
from datetime import datetime

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

# Initialize scrapers
scraper = CinemaBRScraper()
telegraph = TelegraphUploader()

# COMMAND HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    welcome_text = """
🎬 **Bem-vindo ao Cinema BR Indie Bot!**

Eu sou seu assistente pessoal para o cinema independente brasileiro. Envio diariamente um resumo com os principais festivais, editais abertos e notícias do circuito indie.

📌 **O que você encontra aqui:**
✅ Festivais regionais (Nordeste, Sul, Sudeste, Centro-Oeste)
✅ Prazos de submissão de filmes (curtas, longas, docs)
✅ Chamadas públicas e leis de incentivo
✅ Premiações e resultados de festivais
✅ Oportunidades de distribuição e mercado

⚡ **Comandos rápidos:**
/festivais → Veja os festivais em andamento
/submissoes → Prazos abertos para inscrição
/noticias → Últimas notícias do indie BR
/premiados → Filmes premiados na semana
/hoje → Resumo diário (completo)

📖 Para ler a análise completa, clique no link que envio todos os dias.

Boa sorte com sua inscrição! 🍿🎥
    """
    
    keyboard = [
        [
            InlineKeyboardButton("📅 Resumo de Hoje", callback_data="today"),
            InlineKeyboardButton("🎬 Festivais", callback_data="festivals")
        ],
        [
            InlineKeyboardButton("📰 Notícias", callback_data="news"),
            InlineKeyboardButton("🏅 Premiações", callback_data="awards")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def festivals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current festivals"""
    await update.message.reply_text("🔄 Buscando festivais...")
    
    data = scraper.get_festivals()
    if data:
        response = "🏆 **Festivais em Andamento:**\n\n"
        for f in data[:5]:
            response += f"🎬 **{f['name']}**\n"
            response += f"📝 {f['description']}\n"
            response += f"🔗 [Mais informações]({f['link']})\n"
            response += f"⏰ {f['deadline']}\n\n"
        
        # Generate Telegraph article
        telegraph_url = telegraph.create_daily_article({
            'festivals': data,
            'news': scraper.get_news(),
            'awards': scraper.get_awards(),
            'date': datetime.now().strftime('%d/%m/%Y')
        })
        
        if telegraph_url:
            response += f"\n📖 **Leia a análise completa:**\n{telegraph_url}"
        
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Não foi possível buscar festivais no momento. Tente novamente mais tarde.")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show latest news"""
    await update.message.reply_text("🔄 Buscando notícias...")
    
    data = scraper.get_news()
    if data:
        response = "📰 **Últimas Notícias do Cinema BR:**\n\n"
        for n in data[:5]:
            response += f"📌 **{n['title']}**\n"
            response += f"📡 Fonte: {n['source']}\n"
            response += f"🔗 [Leia mais]({n['link']})\n\n"
        
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Não foi possível buscar notícias no momento.")

async def awards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recent awards"""
    data = scraper.get_awards()
    response = "🏅 **Premiações do Cinema Brasileiro:**\n\n"
    for a in data:
        response += f"**{a['name']}**\n"
        response += f"🏷️ Categoria: {a['category']}\n"
        response += f"🏆 {a['winner']}\n"
        response += f"📅 {a['year']}\n\n"
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily summary with Telegraph link"""
    await update.message.reply_text("🔄 Gerando resumo diário...")
    
    data = scraper.get_daily_summary()
    
    # Create Telegraph article
    telegraph_url = telegraph.create_daily_article(data)
    
    if telegraph_url:
        response = f"""
📅 **Resumo do Cinema Independente BR** - {data['date']}

📊 **Resumo:**
• {len(data['festivals'])} festivais em andamento
• {len(data['news'])} notícias atualizadas
• {len(data['awards'])} premiações listadas

📖 **Confira a análise completa:**
{telegraph_url}

🔔 Use /festivais, /noticias ou /premiados para detalhes específicos.
        """
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Erro ao gerar o resumo. Tente novamente mais tarde.")

async def submissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show open submissions"""
    response = """
📅 **Prazos de Submissão Abertos:**

🎬 **Festival de Gramado 2026**
📝 Inscrições abertas para curtas e longas
⏰ Prazo: Verifique site oficial
🔗 https://www.festivaldegramado.net

🎬 **Mostra de Cinema de Tiradentes**
📝 Submissão de filmes independentes
⏰ Prazo: Em breve
🔗 https://www.mostratiradentes.com.br

🎬 **Festival do Rio 2026**
📝 Inscrições para mostras competitivas
⏰ Prazo: Acompanhe site
🔗 https://www.festivaldorio.com.br

🎬 **Cine PE - Festival do Recife**
📝 Inscrições abertas
⏰ Prazo: Verifique site
🔗 https://www.cinepe.com.br

🎬 **Curta Cinema - Festival de Curtas RJ**
📝 Inscrições para curtas-metragens
⏰ Prazo: Acompanhe site
🔗 https://www.curtacinema.com.br

📢 Fique atento aos editais da ANCINE para fomento!
🔗 https://www.gov.br/ancine
    """
    await update.message.reply_text(response, parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks"""
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

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("festivais", festivals))
    application.add_handler(CommandHandler("noticias", news))
    application.add_handler(CommandHandler("premiados", awards))
    application.add_handler(CommandHandler("hoje", today))
    application.add_handler(CommandHandler("submissoes", submissions))
    
    # Callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("🤖 Cinema BR Indie Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
