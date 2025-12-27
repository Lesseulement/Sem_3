from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["🌤️ Погода", "💰 Курс валют"],
        ["📝 Заметки", "⏰ Напоминания"],
        ["🎮 Игры", "🎭 Развлечения"],
        ["⚙️ Настройки", "🆘 Помощь"]
    ], resize_keyboard=True)

def get_weather_keyboard():
    keyboard = [
        [InlineKeyboardButton("Москва", callback_data="weather_moscow"),
         InlineKeyboardButton("Санкт-Петербург", callback_data="weather_spb")],
        [InlineKeyboardButton("Мой город", callback_data="weather_my_city")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_currency_keyboard():
    keyboard = [
        [InlineKeyboardButton("USD/RUB", callback_data="currency_usd"),
         InlineKeyboardButton("EUR/RUB", callback_data="currency_eur")],
        [InlineKeyboardButton("CNY/RUB", callback_data="currency_cny"),
         InlineKeyboardButton("TRY/RUB", callback_data="currency_try")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌍 Язык", callback_data="set_lang")],
        [InlineKeyboardButton("🔔 Уведомления", callback_data="toggle_notifications")],
        [InlineKeyboardButton("🏙️ Мой город", callback_data="set_city")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_games_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎲 Случайное число", callback_data="game_random")],
        [InlineKeyboardButton("🎯 Угадай число", callback_data="game_guess")],
        [InlineKeyboardButton("✂️ Камень-Ножницы-Бумага", callback_data="game_rps")],
        [InlineKeyboardButton("🎮 Викторина", callback_data="game_quiz")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)