"""
Бот-сомелье для Анаконда Навигатор (ПОЛНАЯ МЕГА-ВЕРСИЯ)
Имя бота: SommelierksuBot
Включены все материалы из PDF Елены Горбачевой
"""

import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ТОКЕН ПРЯМО В КОДЕ
BOT_TOKEN = "8624134875:AAFuCFt28W93rjOlBlkwlVGIAzhphTKPHEI"

print("=" * 60)
print("🍷 SOMMELIER BOT - ПОЛНАЯ МЕГА-ВЕРСИЯ")
print("📚 ЗАГРУЗКА ВСЕХ МАТЕРИАЛОВ ИЗ PDF")
print("=" * 60)

# ============================================
# 1. КРАСНЫЕ ВИНА
# ============================================
RED_WINES = {
    "каберне совиньон": {
        "desc": "Король красных вин. Мощное, с танинами. Ароматы черной смородины, табака.",
        "pair": "🥩 Стейк Рибай\n🍖 Баранина\n🧀 Выдержанный Чеддер"
    },
    "пино нуар": {
        "desc": "Элегантное красное вино с ароматом ягод и подлеска.",
        "pair": "🦆 Утка\n🍄 Грибы\n🐟 Лосось\n🧀 Бри"
    },
    "мерло": {
        "desc": "Мягкое красное вино с нотами сливы и шоколада.",
        "pair": "🍗 Курица\n🍔 Мясное рагу\n🧀 Мягкие сыры"
    },
    "шираз": {
        "desc": "Пряное красное вино с нотами черного перца.",
        "pair": "🌶 Острые блюда\n🔥 Стейк\n🍖 Барбекю"
    },
    "мальбек": {
        "desc": "Бархатистое красное вино из Аргентины.",
        "pair": "🥩 Стейк\n🍖 Барбекю\n🧀 Выдержанный Чеддер"
    },
    "темпранильо": {
        "desc": "Испанское красное вино, основа Риохи.",
        "pair": "🇪🇸 Паэлья\n🥩 Хамон\n🍅 Томатные соусы"
    },
    "санджовезе": {
        "desc": "Главный сорт Тосканы, основа Кьянти.",
        "pair": "🍝 Паста Болоньезе\n🍕 Пицца\n🧀 Пармезан"
    },
    "неббиоло": {
        "desc": "Великое вино Пьемонта. Мощные танины.",
        "pair": "🍄 Трюфели\n🥩 Тушеная говядина\n🍖 Дичь"
    },
    "барбера": {
        "desc": "Пьемонтское вино с низкими танинами.",
        "pair": "🥓 Прошутто\n🍝 Паста с мясом\n🍖 Свинина"
    },
    "зинфандель": {
        "desc": "Американская классика. Высокий алкоголь.",
        "pair": "🌶 Острые блюда\n🍔 Бургеры\n🍖 Свиные ребрышки"
    },
    "карменер": {
        "desc": "Чилийская гордость. Ароматы перца и шоколада.",
        "pair": "🥩 Стейк\n🍖 Шашлык\n🌶 Острые блюда"
    },
    "примитиво": {
        "desc": "Южная Италия. Мощное, пряное.",
        "pair": "🍖 Мясо на гриле\n🌶 Колбаски\n🧀 Выдержанные сыры"
    },
    "гаме": {
        "desc": "Сорт Божоле. Легкое, фруктовое.",
        "pair": "🥓 Мясные нарезки\n🐟 Рыба на гриле\n🥗 Легкие салаты"
    },
    "каберне фран": {
        "desc": "Травянистый, с нотами перца и фиалки.",
        "pair": "🥓 Козьи сыры\n🥘 Овощное рагу\n🌿 Блюда с травами"
    },
    "блауфранкиш": {
        "desc": "Австрийская классика. Пряное.",
        "pair": "🥓 Утиный паштет\n🍖 Свинина\n🍗 Курица"
    },
    "кьянти": {
        "desc": "Тосканское красное. Высокая кислотность.",
        "pair": "🍝 Паста с томатами\n🥩 Бистекка\n🍕 Пицца"
    },
    "брунелло": {
        "desc": "Великое тосканское вино. Мощное.",
        "pair": "🥩 Стейк\n🍖 Дичь\n🧀 Пармезан"
    },
    "вальполичелла": {
        "desc": "Веронское красное. Легкое, вишневое.",
        "pair": "🥓 Прошутто\n🍝 Паста\n🍖 Свинина"
    },
    "амароне": {
        "desc": "Мощное веронское из подвяленного винограда.",
        "pair": "🍖 Дичь\n🧀 Выдержанные сыры\n🍫 Шоколад"
    },
    "бароло": {
        "desc": "Великое пьемонтское. Мощное, танинное.",
        "pair": "🍄 Трюфели\n🥩 Тушеная говядина\n🍖 Дичь"
    }
}

# ============================================
# 2. БЕЛЫЕ ВИНА
# ============================================
WHITE_WINES = {
    "шардоне": {
        "desc": "Самое популярное белое вино. Дубовое или свежее.",
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
    "пино гриджо": {
        "desc": "Легкое, нейтральное белое вино.",
        "pair": "🥗 Легкие салаты\n🐟 Белая рыба\n🍋 Лимонные десерты"
    },
    "альбариньо": {
        "desc": "Галисийское белое. Минеральное, солоноватое.",
        "pair": "🦪 Устрицы\n🦐 Креветки\n🐟 Рыба"
    },
    "гевюрцтраминер": {
        "desc": "Ароматное вино с нотами розы и специй.",
        "pair": "🥘 Азиатская кухня\n🧀 Мюнстер\n🦆 Фуа-гра"
    },
    "шенен блан": {
        "desc": "Универсальный сорт Луары. От сухого до сладкого.",
        "pair": "🍏 Яблочные десерты\n🧀 Козьи сыры\n🐟 Рыба"
    },
    "вионье": {
        "desc": "Ароматное, полнотелое с нотами персика.",
        "pair": "🥭 Блюда с персиками\n🦞 Омары\n🐔 Курица"
    },
    "верментино": {
        "desc": "Итальянское прибрежное. Свежее, минеральное.",
        "pair": "🦐 Морепродукты\n🐟 Рыба\n🥗 Салаты"
    },
    "вердехо": {
        "desc": "Испанское из Руэды. Свежее, травянистое.",
        "pair": "🥗 Легкие салаты\n🐟 Рыба\n🦐 Креветки"
    },
    "гави": {
        "desc": "Главное рыбное вино Италии.",
        "pair": "🦞 Омары\n🐟 Рыба\n🦐 Морепродукты"
    },
    "грюнер вельтлинер": {
        "desc": "Австрийская классика. Пряное, минеральное.",
        "pair": "🌱 Спаржа\n🦪 Устрицы\n🥗 Зеленые салаты"
    },
    "мускат": {
        "desc": "Ароматное вино с нотами цветов.",
        "pair": "🍑 Фруктовые десерты\n🍰 Легкие пирожные"
    },
    "соаве": {
        "desc": "Белое из Венето. Миндальное.",
        "pair": "🐟 Рыба\n🥗 Салаты\n🦐 Креветки"
    }
}

# ============================================
# 3. ИГРИСТЫЕ ВИНА
# ============================================
SPARKLING_WINES = {
    "шампанское": {
        "desc": "Король игристых. Пузырьки и кислотность.",
        "pair": "🦪 Устрицы\n🍓 Клубника\n🧀 Бри"
    },
    "просекко": {
        "desc": "Легкое итальянское игристое.",
        "pair": "🍕 Закуски\n🫒 Оливки\n🍰 Десерты"
    },
    "кава": {
        "desc": "Испанское игристое. Кислотное, свежее.",
        "pair": "🇪🇸 Паэлья\n🍤 Креветки\n🥗 Салаты"
    },
    "франчакорта": {
        "desc": "Итальянское игристое из Ломбардии.",
        "pair": "🥩 Ростбиф\n🐟 Тунец\n🧀 Выдержанные сыры"
    },
    "блан де блан": {
        "desc": "Шампанское из 100% Шардоне. Элегантное.",
        "pair": "🦪 Устрицы\n🍣 Суши\n🦐 Ракообразные"
    },
    "блан де нуар": {
        "desc": "Шампанское из красных сортов.",
        "pair": "🍗 Пироги\n🥓 Фуа-гра\n🐔 Курица"
    },
    "розе шампанское": {
        "desc": "Игристое розе с нотами красных ягод.",
        "pair": "🍓 Клубника\n🦞 Омары\n🦆 Утка"
    },
    "асти": {
        "desc": "Сладкое итальянское игристое из Муската.",
        "pair": "🍰 Десерты\n🍑 Персики\n🍊 Апельсины"
    },
    "ламбруско": {
        "desc": "Итальянское красное игристое.",
        "pair": "🍕 Пицца\n🍝 Паста\n🥓 Мясные закуски"
    }
}

# ============================================
# 4. КРЕПЛЕНЫЕ ВИНА
# ============================================
FORTIFIED_WINES = {
    "портвейн руби": {
        "desc": "Молодой портвейн, яркий, ягодный.",
        "pair": "🧀 Горгонзола\n🍫 Шоколадный мусс\n🍓 Ягоды"
    },
    "портвейн тони": {
        "desc": "Выдержанный портвейн. Ноты орехов.",
        "pair": "🦆 Фуа-гра\n🧀 Чеддер\n🌰 Орехи"
    },
    "херес фино": {
        "desc": "Сухой херес. Легкий, солоноватый.",
        "pair": "🇪🇸 Тапас\n🫒 Оливки\n🥩 Хамон"
    },
    "херес олоросо": {
        "desc": "Насыщенный херес с нотами орехов.",
        "pair": "🥘 Мясное рагу\n🍖 Дичь\n🧀 Выдержанные сыры"
    },
    "херес педро хименес": {
        "desc": "Сладчайший херес. Ноты фиников, шоколада.",
        "pair": "🧀 Голубые сыры\n🍫 Шоколадные десерты"
    },
    "мадера": {
        "desc": "Крепленое с Мадейры. Ноты карамели.",
        "pair": "🍄 Грибной суп\n🍰 Тирамису\n🍊 Апельсины"
    },
    "марсала": {
        "desc": "Сицилийское крепленое.",
        "pair": "🍰 Тирамису\n🧀 Пекорино\n🍫 Шоколад"
    },
    "вермут": {
        "desc": "Ароматизированное крепленое с травами.",
        "pair": "🥩 Холодная телятина\n🥓 Ветчина\n🫒 Оливки"
    }
}

# ============================================
# 5. РОЗОВЫЕ ВИНА
# ============================================
ROSE_WINES = {
    "прованс розе": {
        "desc": "Эталон розовых вин. Бледные, сухие.",
        "pair": "🥗 Зеленые салаты\n🦐 Севиче\n🐟 Рыба на гриле"
    },
    "тавель": {
        "desc": "Розе из долины Роны. Плотное, пряное.",
        "pair": "🌮 Пряные блюда\n🍖 Мясные закуски\n🧀 Козьи сыры"
    },
    "риоха розе": {
        "desc": "Испанское розе из Темпранильо.",
        "pair": "🥓 Паштеты\n🐔 Курица\n🐟 Тунец"
    },
    "анжу розе": {
        "desc": "Французское розе из Луары.",
        "pair": "🍓 Ягоды\n🍰 Десерты\n🥗 Салаты"
    }
}

# ============================================
# 6. ОРАНЖЕВЫЕ ВИНА
# ============================================
ORANGE_WINES = {
    "оранжевое вино": {
        "desc": "Белые вина по красному методу. Танинные.",
        "pair": "🍖 Шашлык\n🍄 Грибы\n🧀 Сырная тарелка"
    },
    "грузинское янтарное": {
        "desc": "Грузинские вина в квеври. Мощные.",
        "pair": "🍖 Шашлык\n🥗 Баклажаны с орехами\n🧀 Сулугуни"
    }
}

# ============================================
# 7. ФРАНЦУЗСКИЕ ВИНА
# ============================================
FRENCH_WINES = {
    "бордо красное": {
        "desc": "Ассамбляж Каберне и Мерло.",
        "pair": "🥩 Стейк\n🍖 Баранина\n🧀 Сыры"
    },
    "бордо белое": {
        "desc": "Ассамбляж Семильона и Совиньон Блан.",
        "pair": "🦞 Омары\n🐟 Рыба\n🧀 Сыры"
    },
    "сотерн": {
        "desc": "Сладкое белое из Бордо.",
        "pair": "🦆 Фуа-гра\n🧀 Рокфор\n🍑 Персики"
    },
    "бургундия красное": {
        "desc": "Пино Нуар из Бургундии.",
        "pair": "🦆 Утка\n🍄 Грибы\n🐟 Лосось"
    },
    "бургундия белое": {
        "desc": "Шардоне из Бургундии.",
        "pair": "🦞 Омары\n🐟 Палтус\n🧀 Сыры"
    },
    "шабли": {
        "desc": "Шардоне из Шабли. Минеральное.",
        "pair": "🦪 Устрицы\n🐟 Рыба\n🦐 Креветки"
    },
    "сансер": {
        "desc": "Совиньон Блан из Луары.",
        "pair": "🐐 Козий сыр\n🦪 Устрицы\n🌱 Спаржа"
    }
}

# ============================================
# 8. ИСПАНСКИЕ ВИНА
# ============================================
SPANISH_WINES = {
    "альбариньо галисия": {
        "desc": "Галисийское белое. Соленые ноты.",
        "pair": "🦪 Устрицы\n🦐 Морепродукты\n🐟 Рыба"
    },
    "темпранильо риоха": {
        "desc": "Красное Риохи. Ноты ванили.",
        "pair": "🥩 Красное мясо\n🍖 Баранина\n🥘 Паэлья"
    },
    "риоха белая": {
        "desc": "Белое Риохи с выдержкой в дубе.",
        "pair": "🇪🇸 Паэлья с морепродуктами\n🐟 Рыба"
    },
    "вердехо руэда": {
        "desc": "Белое из Руэды. Свежее, травянистое.",
        "pair": "🥗 Легкие салаты\n🦐 Морепродукты"
    },
    "херес": {
        "desc": "Хересы всех типов с тапас.",
        "pair": "🫒 Оливки\n🥩 Хамон\n🧀 Сыры"
    },
    "кава испания": {
        "desc": "Испанское игристое.",
        "pair": "🍰 Десерты\n🍓 Ягоды\n🥐 Выпечка"
    }
}

# ============================================
# 9. СЫРЫ
# ============================================
CHEESE_PAIRINGS = {
    "козий сыр": "🥂 Совиньон Блан, Шенен Блан",
    "бри": "🍷 Пино Нуар, 🥂 Шампанское",
    "камамбер": "🍷 Пино Нуар, 🥂 Шампанское",
    "рокфор": "🍾 Сотерн, Портвейн",
    "пармезан": "🍷 Брунелло, Санджовезе",
    "чеддер": "🍷 Каберне Совиньон, Мальбек",
    "горгонзола": "🍾 Портвейн",
    "моцарелла": "🥂 Пино Гриджо",
    "фета": "🥂 Совиньон Блан"
}

# ============================================
# 10. РЫБА
# ============================================
SEAFOOD_PAIRINGS = {
    "устрицы": "🥂 Шабли, Шампанское, Альбариньо",
    "лосось": "🍷 Пино Нуар, 🥂 Шардоне",
    "тунец": "🍷 Пино Нуар, 🥂 Совиньон Блан",
    "креветки": "🥂 Альбариньо, Совиньон Блан",
    "омары": "🥂 Шампанское, Шардоне",
    "гребешки": "🥂 Шампанское, Сансер",
    "мидии": "🥂 Альбариньо, Мюскаде",
    "икра": "🥂 Шампанское"
}

# ============================================
# 11. МЯСО
# ============================================
MEAT_PAIRINGS = {
    "стейк": "🍷 Каберне Совиньон, Мальбек",
    "баранина": "🍷 Каберне Совиньон",
    "свинина": "🥂 Рислинг, 🍷 Пино Нуар",
    "утка": "🍷 Пино Нуар",
    "курица": "🥂 Шардоне, 🍷 Пино Нуар",
    "шашлык": "🍷 Карменер, Каберне",
    "бургер": "🍷 Мальбек, Зинфандель"
}

# ============================================
# 12. ОВОЩИ
# ============================================
VEGETABLE_PAIRINGS = {
    "спаржа": "🥂 Совиньон Блан",
    "грибы": "🍷 Пино Нуар",
    "томаты": "🍷 Кьянти",
    "баклажаны": "🍷 Кьянти, 🥂 розе",
    "тыква": "🥂 Гевюрцтраминер"
}

# ============================================
# 13. ДЕСЕРТЫ
# ============================================
DESSERT_PAIRINGS = {
    "шоколад": "🍾 Портвейн",
    "чизкейк": "🥂 Сотерн",
    "яблочный пирог": "🥂 Рислинг",
    "тирамису": "🍾 Марсала",
    "клубника": "🥂 розе, 🍷 Пино Нуар"
}

# ============================================
# 14. РУССКАЯ КУХНЯ
# ============================================
RUSSIAN_CUISINE = {
    "оливье": "🥂 Шампанское",
    "селедка под шубой": "🥂 розе",
    "соленья": "🥂 Шампанское",
    "винегрет": "🥂 Совиньон Блан",
    "маринованные грибы": "🥂 Шардоне",
    "пельмени": "🥂 Рислинг",
    "борщ": "🍷 Красностоп"
}

# ============================================
# ОБЪЕДИНЯЕМ ВСЕ ВИНА
# ============================================
ALL_WINES = {}
ALL_WINES.update(RED_WINES)
ALL_WINES.update(WHITE_WINES)
ALL_WINES.update(SPARKLING_WINES)
ALL_WINES.update(FORTIFIED_WINES)
ALL_WINES.update(ROSE_WINES)
ALL_WINES.update(ORANGE_WINES)
ALL_WINES.update(FRENCH_WINES)
ALL_WINES.update(SPANISH_WINES)

print(f"📊 ЗАГРУЖЕНО: {len(ALL_WINES)} ВИН")
print("=" * 60)

# ============================================
# КЛАВИАТУРЫ
# ============================================
def get_main_keyboard():
    keyboard = [
        ["🍷 Красные", "🥂 Белые"],
        ["✨ Игристые", "🍾 Крепленые"],
        ["🌸 Розовые", "🟠 Оранжевые"],
        ["🇫🇷 Французские", "🇪🇸 Испанские"],
        ["🧀 Сыры", "🐟 Рыба"],
        ["🍖 Мясо", "🥗 Овощи"],
        ["🍰 Десерты", "🇷🇺 Русская"],
        ["❌ Отмена"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_search_keyboard():
    keyboard = [
        ["🧀 Сыры", "🐟 Рыба"],
        ["🍖 Мясо", "🥗 Овощи"],
        ["🍰 Десерты", "🇷🇺 Русская"],
        ["🔙 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ============================================
# ОБРАБОТЧИКИ
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🍷 *Привет, {user.first_name}!*\n\n"
        f"📚 В базе: {len(ALL_WINES)} вин\n"
        f"👇 *Выбери категорию:*",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text_lower = text.lower().strip()
    
    # Навигация
    if text == "🔙 Главное меню":
        await update.message.reply_text("Главное меню:", reply_markup=get_main_keyboard())
        return
    
    if text == "❌ Отмена":
        await update.message.reply_text("До встречи! /start", 
                                       reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True))
        return
    
    # Категории вин
    if text == "🍷 Красные":
        wines = list(RED_WINES.keys())
        response = "🍷 *Красные вина:*\n\n"
        for w in sorted(wines)[:10]:
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🥂 Белые":
        wines = list(WHITE_WINES.keys())
        response = "🥂 *Белые вина:*\n\n"
        for w in sorted(wines)[:10]:
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "✨ Игристые":
        wines = list(SPARKLING_WINES.keys())
        response = "✨ *Игристые вина:*\n\n"
        for w in sorted(wines):
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🍾 Крепленые":
        wines = list(FORTIFIED_WINES.keys())
        response = "🍾 *Крепленые вина:*\n\n"
        for w in sorted(wines):
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🌸 Розовые":
        wines = list(ROSE_WINES.keys())
        response = "🌸 *Розовые вина:*\n\n"
        for w in sorted(wines):
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🟠 Оранжевые":
        wines = list(ORANGE_WINES.keys())
        response = "🟠 *Оранжевые вина:*\n\n"
        for w in sorted(wines):
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🇫🇷 Французские":
        wines = list(FRENCH_WINES.keys())
        response = "🇫🇷 *Французские вина:*\n\n"
        for w in sorted(wines):
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🇪🇸 Испанские":
        wines = list(SPANISH_WINES.keys())
        response = "🇪🇸 *Испанские вина:*\n\n"
        for w in sorted(wines):
            response += f"• {w.title()}\n"
        response += "\nНапиши название вина"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    if text == "🇷🇺 Русская":
        response = "🇷🇺 *Русская кухня:*\n\n"
        for dish, wine in list(RUSSIAN_CUISINE.items())[:8]:
            response += f"• {dish.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return
    
    # Поиск по еде
    if text == "🧀 Сыры":
        response = "🧀 *Сыры:*\n\n"
        for cheese, wine in CHEESE_PAIRINGS.items():
            response += f"• {cheese.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_search_keyboard())
        return
    
    if text == "🐟 Рыба":
        response = "🐟 *Рыба:*\n\n"
        for fish, wine in SEAFOOD_PAIRINGS.items():
            response += f"• {fish.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_search_keyboard())
        return
    
    if text == "🍖 Мясо":
        response = "🍖 *Мясо:*\n\n"
        for meat, wine in MEAT_PAIRINGS.items():
            response += f"• {meat.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_search_keyboard())
        return
    
    if text == "🥗 Овощи":
        response = "🥗 *Овощи:*\n\n"
        for veg, wine in VEGETABLE_PAIRINGS.items():
            response += f"• {veg.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_search_keyboard())
        return
    
    if text == "🍰 Десерты":
        response = "🍰 *Десерты:*\n\n"
        for dessert, wine in DESSERT_PAIRINGS.items():
            response += f"• {dessert.title()}: {wine}\n"
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_search_keyboard())
        return
    
    # Поиск по конкретным продуктам
    all_food_pairs = {
        **CHEESE_PAIRINGS, **SEAFOOD_PAIRINGS, **MEAT_PAIRINGS, 
        **VEGETABLE_PAIRINGS, **DESSERT_PAIRINGS, **RUSSIAN_CUISINE
    }
    
    for food, wine in all_food_pairs.items():
        if food in text_lower:
            await update.message.reply_text(
                f"🍽 *{food.title()}*\n\n🍷 *Рекомендация:* {wine}",
                parse_mode='Markdown',
                reply_markup=get_search_keyboard()
            )
            return
    
    # Поиск по винам
    for wine_name, wine_info in ALL_WINES.items():
        if wine_name in text_lower or text_lower in wine_name:
            await update.message.reply_text(
                f"🍷 *{wine_name.title()}*\n"
                f"_{wine_info['desc']}_\n\n"
                f"🍽 *Гастропара:*\n{wine_info['pair']}",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
            return
    
    # Если ничего не найдено
    await update.message.reply_text(
        "😕 Не найдено. Выбери из меню!",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🍷 *Помощь*\n\n"
        "/start - Начать\n"
        "Выбирай категории из меню\n"
        "Или пиши название вина/блюда\n\n"
        f"📚 Всего вин: {len(ALL_WINES)}",
        parse_mode='Markdown'
    )

# ============================================
# ЗАПУСК
# ============================================
def main():
    print("=" * 60)
    print("🍷 SOMMELIER BOT - ПОЛНАЯ ВЕРСИЯ")
    print(f"📊 ВСЕГО ВИН: {len(ALL_WINES)}")
    print("=" * 60)
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ БОТ ЗАПУЩЕН!")
    app.run_polling()

if __name__ == "__main__":
    main()
