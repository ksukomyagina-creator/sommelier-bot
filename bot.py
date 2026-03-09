"""
Бот-сомелье для Railway (исправленная версия)
Имя бота: SommelierksuBot
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# База вин
WINES = {
    "каберне совиньон": "🥩 Стейк, баранина, выдержанный сыр",
    "пино нуар": "🦆 Утка, грибы, лосось, бри",
    "рислинг": "🥘 Тайская кухня, морепродукты, рыба",
    "шампанское": "🦪 Устрицы, клубника, бри",
    "шардоне": "🦞 Омары, паста карбонара, курица",
    "совиньон блан": "🐐 Козий сыр, спаржа, устрицы"
}

def get_keyboard():
    wines = sorted(WINES.keys())
    keyboard = []
    row = []
    for i, wine in enumerate(wines):
        row.append(wine.title())
        if (i + 1) % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍷 Привет! Я бот-сомелье. Выбери вино:",
        reply_markup=get_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    
    for wine, pairing in WINES.items():
        if wine in text:
            await update.message.reply_text(
                f"🍷 *{wine.title()}*\n\n🍽 *Идеальная пара:*\n{pairing}",
                parse_mode='Markdown',
                reply_markup=get_keyboard()
            )
            return
    
    await update.message.reply_text(
        "😕 Вино не найдено. Выбери из списка:",
        reply_markup=get_keyboard()
    )

def main():
    print("Запуск бота...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
