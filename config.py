import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Токен бота от @BotFather
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # Настройки администратора
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

    # Настройки базы данных
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")

    # API ключи для внешних сервисов
    OPENWEATHER_API = os.getenv("OPENWEATHER_API", "")
    EXCHANGE_API = os.getenv("EXCHANGE_API", "")

    # Настройки бота
    BOT_USERNAME = ""
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

    # Команды бота
    COMMANDS = [
        ("start", "Запустить бота"),
        ("help", "Помощь по командам"),
        ("weather", "Погода в вашем городе"),
        ("currency", "Курсы валют"),
        ("poll", "Создать опрос"),
        ("reminder", "Установить напоминание"),
        ("joke", "Случайная шутка"),
        ("calc", "Калькулятор"),
        ("news", "Последние новости"),
        ("profile", "Мой профиль"),
        ("admin", "Панель администратора"),
    ]