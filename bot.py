"""
Бот-сомелье для Анаконда Навигатор (ПОЛНАЯ ВЕРСИЯ)
Имя бота: SommelierksuBot
"""

import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ТОКЕН ПРЯМО В КОДЕ
BOT_TOKEN = "8624134875:AAFuCFt28W93rjOlBlkwlVGIAzhphTKPHEI"

print("🚀 ЗАПУСК ПОЛНОЙ ВЕРСИИ SOMMELIER BOT")

# ============================================
# ПОЛНАЯ БАЗА ЗНАНИЙ (сокращенная версия для начала, но рабочая)
# ============================================

WINES = {
    "каберне совиньон": {
        "desc": "Король красных вин. Мощное, с танинами.",
        "pair": "🥩 Стейк Рибай\n🍖 Баранина\n🧀 Выдержанный Чеддер"
    },
    "пино нуар": {
        "desc": "Элегантное красное вино с ароматом ягод.",
        "pair": "🦆 Утка\n🍄 Грибы\n🐟 Лосось\n🧀 Бри"
    },
    "мерло": {
        "desc": "Мягкое красное вино с нотами сливы.",
        "pair": "🍗 Курица\n🍔 Мясное рагу\n🧀 Мягкие сыры"
    },
    "шираз": {
        "desc": "Пряное красное вино с нотами перца.",
        "pair": "🌶 Острые блюда\n🔥 Стейк\n🍖 Барбекю"
    },
    "шардоне": {
        "desc": "Белое вино. Бывает дубовым и свежим.",
        "pair": "🦞 Омары\n🍝 Паста Карбонара\n🐔 Курица"
    },
    "совиньон блан": {
        "desc": "Свежее, травянистое белое вино.",
        "pair": "🐐 Козий сыр\n🌱 Спаржа\n🦪 Устрицы"
    },
    "рислинг": {
        "desc": "Белое вино с высокой кислотностью.",
        "pair": "🥘 Тайская кухня\n🦐 Морепродукты\n🐟 Рыба"
    },
    "шампанское": {
        "desc": "Король игристых. Пузырьки.",
        "pair": "🦪 Устрицы\n🍓 Клубника\n🧀 Бри"
    }
}

# КАТЕГОРИИ ПО ЕДЕ
CHEESES = {
    "козий сыр": "🥂 Совиньон Блан",
    "бри": "🍷 Пино Нуар, 🥂 Шампанское",
    "пармезан": "🍷 Санджовезе"
}

SEAFOOD = {
    "устрицы": "🥂 Шабли, 🥂 Шампанское",
    "лосось": "🍷 Пино Нуар, 🥂 Шардоне",
    "креветки": "🥂 Альбариньо"
}

def get_main_keyboard():
    keyboard = [
        ["🍷 Красные", "🥂 Белые"],
        ["✨ Игристые", "🔍 Поиск по еде"],
        ["❌ Отмена"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_food_keyboard():
    keyboard = [
        ["🧀 Сыры", "🐟 Рыба"],
        ["🍖 Мясо", "🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🍷 *Привет, {user.first_name}!*\n\n"
        f"В базе: {len(WINES)} вин\n"
        f"Выбери категорию:",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text_lower = text.lower().strip()
    
    if text == "🏠 Главное меню":
        await update.message.reply_text("Главное меню:", reply_markup=get_main_keyboard())
        return
    
    if text == "❌ Отмена":
        await update.message.reply_text("До встречи!", reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True))
        return
    
    if text == "🍷 Красные":
        wines = ["каберне совиньон", "пино нуар", "мерло", "шираз"]
        response = "🍷 *Красные вина:*\n\n"
        for w in wines:
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🥂 Белые":
        wines = ["шардоне", "совиньон блан", "рислинг"]
        response = "🥂 *Белые вина:*\n\n"
        for w in wines:
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "✨ Игристые":
        wines = ["шампанское"]
        response = "✨ *Игристые вина:*\n\n"
        for w in wines:
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🔍 Поиск по еде":
        await update.message.reply_text("Выбери категорию:", reply_markup=get_food_keyboard())
        return
    
    if text == "🧀 Сыры":
        response = "🧀 *Сыры:*\n\n"
        for cheese, wine in CHEESES.items():
            response += f"• {cheese.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_food_keyboard())
        return
    
    if text == "🐟 Рыба":
        response = "🐟 *Рыба:*\n\n"
        for fish, wine in SEAFOOD.items():
            response += f"• {fish.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_food_keyboard())
        return
    
    # Поиск вина
    for wine_name, wine_info in WINES.items():
        if wine_name in text_lower:
            await update.message.reply_text(
                f"🍷 *{wine_name.title()}*\n"
                f"_{wine_info['desc']}_\n\n"
                f"🍽 *Гастропара:*\n{wine_info['pair']}",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
            return
    
    await update.message.reply_text("Не найдено. Выбери из меню!", reply_markup=get_main_keyboard())

def main():
    print("✅ Запуск...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
