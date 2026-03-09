"""
Бот-сомелье для Railway
Имя бота: SommelierksuBot
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Получаем токен из переменных окружения (безопасно!)
BOT_TOKEN = os.environ.get('BOT_TOKEN', "8624134875:AAFuCFt28W93rjOlBlkwlVGIAzhphTKPHEI")

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# База вин (небольшая для начала)
WINES = {
    "каберне совиньон": {
        "description": "Король красных вин. Мощное, с танинами.",
        "pairing": "🥩 Стейк Рибай\n🍖 Баранина\n🧀 Выдержанный Чеддер",
        "reason": "Танины смягчаются животными белками."
    },
    "пино нуар": {
        "description": "Элегантное красное вино с ароматом ягод.",
        "pairing": "🦆 Утка\n🍄 Грибы\n🐟 Лосось",
        "reason": "Нежная структура дополняет изысканные вкусы."
    },
    "рислинг": {
        "description": "Белое вино с высокой кислотностью.",
        "pairing": "🥘 Тайская кухня\n🦐 Морепродукты\n🐟 Рыба",
        "reason": "Кислотность балансирует остроту."
    },
    "шампанское": {
        "description": "Король игристых. Пузырьки и кислотность.",
        "pairing": "🦪 Устрицы\n🍓 Клубника\n🧀 Бри",
        "reason": "Пузырьки очищают вкусовые рецепторы."
    }
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
    keyboard.append(["❌ Отмена"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🍷 *Привет, {user.first_name}!*\nВыбери вино:",
        parse_mode='Markdown',
        reply_markup=get_keyboard()
    )
    return 1

async def handle_wine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    
    if text == "❌ отмена":
        await update.message.reply_text("Пока!", reply_markup=ReplyKeyboardRemove())
        return -1
    
    for key, data in WINES.items():
        if key in text or text in key:
            response = (
                f"🍷 *{key.title()}*\n"
                f"_{data['description']}_\n\n"
                f"🍽 *Гастропара:*\n{data['pairing']}\n\n"
                f"✨ *Почему:*\n{data['reason']}"
            )
            await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_keyboard())
            return 1
    
    await update.message.reply_text("😕 Не найдено. Выбери из списка:", reply_markup=get_keyboard())
    return 1

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('До свидания!', reply_markup=ReplyKeyboardRemove())
    return -1

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wine)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('help', lambda u,c: u.message.reply_text(
        "/start - Начать\n/help - Помощь\n/cancel - Выйти")))
    
    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
