import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ТОКЕН ПРЯМО В КОДЕ
BOT_TOKEN = "8624134875:AAFuCFt28W93rjOlBlkwlVGIAzhphTKPHEI"

print("🚀 ЗАПУСК ТЕСТОВОГО БОТА")
print(f"ТОКЕН: {BOT_TOKEN[:10]}...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ БОТ РАБОТАЕТ! Отправь любое сообщение")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

def main():
    print("Создаю приложение...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("✅ Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
