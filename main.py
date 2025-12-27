import logging
from telegram import Update, ParseMode
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    CallbackQueryHandler, ConversationHandler
)
from telegram.ext.callbackcontext import CallbackContext
import config
from database import init_db, get_or_create_user, Session
from keyboards import *
from utils import *
from datetime import datetime, timedelta
import random

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
CITY, NOTE_TEXT, REMINDER_TEXT, REMINDER_TIME = range(4)


class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.config = config.Config()
        self.init_handlers()

    def init_handlers(self):
        """Инициализация обработчиков команд"""

        # Обработчики команд
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("weather", self.weather_command))
        self.dispatcher.add_handler(CommandHandler("currency", self.currency_command))
        self.dispatcher.add_handler(CommandHandler("joke", self.joke_command))
        self.dispatcher.add_handler(CommandHandler("news", self.news_command))
        self.dispatcher.add_handler(CommandHandler("calc", self.calc_command))
        self.dispatcher.add_handler(CommandHandler("profile", self.profile_command))
        self.dispatcher.add_handler(CommandHandler("admin", self.admin_command))

        # Обработчики сообщений
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))

        # Обработчики inline кнопок
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_handler))

        # Обработчик ошибок
        self.dispatcher.add_error_handler(self.error_handler)

    def start_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /start"""
        user = update.effective_user
        update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n"
            f"Я — многофункциональный бот с полезными функциями.\n\n"
            f"Что я умею:\n"
            f"• 🌤️ Показывать погоду\n"
            f"• 💰 Конвертировать валюты\n"
            f"• 📝 Сохранять заметки\n"
            f"• ⏰ Напоминать о событиях\n"
            f"• 🎮 Играть в игры\n"
            f"• 🎭 Рассказывать шутки\n"
            f"• 📰 Показывать новости\n\n"
            f"Используй меню или команду /help",
            reply_markup=get_main_keyboard()
        )

        # Сохраняем пользователя в БД
        with Session() as session:
            get_or_create_user(
                session,
                user.id,
                user.username,
                user.first_name,
                user.last_name
            )

    def help_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /help"""
        help_text = "📋 Доступные команды:\n\n"
        for cmd, desc in self.config.COMMANDS:
            help_text += f"/{cmd} - {desc}\n"

        help_text += "\n📱 Также доступно меню с кнопками!"
        update.message.reply_text(help_text)

    def weather_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /weather"""
        update.message.reply_text(
            "Выберите город для просмотра погоды:",
            reply_markup=get_weather_keyboard()
        )

    def currency_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /currency"""
        update.message.reply_text(
            "Выберите валютную пару:",
            reply_markup=get_currency_keyboard()
        )

    def joke_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /joke"""
        joke = JokesAPI.get_random_joke()
        update.message.reply_text(f"🎭 {joke}")

    def news_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /news"""
        news = NewsAPI.get_news()
        update.message.reply_text(news)

    def calc_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /calc"""
        update.message.reply_text(
            "Введите математическое выражение для расчета:\n"
            "Например: 2+2*3 или (5+3)/2"
        )
        context.user_data['waiting_for_calc'] = True

    def profile_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /profile"""
        user = update.effective_user

        with Session() as session:
            db_user = session.query(User).filter_by(telegram_id=user.id).first()

            if db_user:
                profile_text = (
                    f"👤 Ваш профиль:\n\n"
                    f"🆔 ID: {db_user.telegram_id}\n"
                    f"👤 Имя: {db_user.first_name} {db_user.last_name or ''}\n"
                    f"📛 Юзернейм: @{db_user.username or 'не указан'}\n"
                    f"📅 Дата регистрации: {db_user.join_date.strftime('%d.%m.%Y')}\n"
                    f"🌍 Город: {db_user.city or 'не указан'}\n"
                    f"🔔 Уведомления: {'включены' if db_user.notifications else 'выключены'}\n"
                    f"👑 Админ: {'да' if db_user.is_admin else 'нет'}"
                )
                update.message.reply_text(profile_text)

    def admin_command(self, update: Update, context: CallbackContext):
        """Обработчик команды /admin"""
        user_id = update.effective_user.id

        if user_id == self.config.ADMIN_ID:
            with Session() as session:
                total_users = session.query(User).count()
                today = datetime.utcnow().date()
                new_today = session.query(User).filter(
                    User.join_date >= today
                ).count()

            admin_text = (
                f"👑 Панель администратора\n\n"
                f"📊 Статистика:\n"
                f"• Всего пользователей: {total_users}\n"
                f"• Новых сегодня: {new_today}\n\n"
                f"⚙️ Команды админа:\n"
                f"/broadcast - Рассылка сообщения\n"
                f"/stats - Подробная статистика\n"
                f"/user_info - Инфо о пользователе"
            )
            update.message.reply_text(admin_text)
        else:
            update.message.reply_text("⛔ У вас нет прав администратора!")

    def handle_message(self, update: Update, context: CallbackContext):
        """Обработчик текстовых сообщений"""
        text = update.message.text

        if context.user_data.get('waiting_for_calc'):
            result = Calculator.calculate(text)
            update.message.reply_text(result)
            context.user_data['waiting_for_calc'] = False
            return

        # Обработка кнопок главного меню
        if text == "🌤️ Погода":
            self.weather_command(update, context)
        elif text == "💰 Курс валют":
            self.currency_command(update, context)
        elif text == "🎭 Развлечения":
            update.message.reply_text(
                "Выберите развлечение:",
                reply_markup=get_games_keyboard()
            )
        elif text == "⚙️ Настройки":
            update.message.reply_text(
                "Настройки бота:",
                reply_markup=get_settings_keyboard()
            )
        elif text == "🆘 Помощь":
            self.help_command(update, context)
        else:
            update.message.reply_text(
                f"Вы написали: {text}\n"
                f"Используйте меню или команду /help"
            )

    def button_handler(self, update: Update, context: CallbackContext):
        """Обработчик нажатий на inline кнопки"""
        query = update.callback_query
        query.answer()

        data = query.data

        if data.startswith("weather_"):
            city = data.split("_")[1]
            if city == "my_city":
                with Session() as session:
                    user = session.query(User).filter_by(
                        telegram_id=query.from_user.id
                    ).first()
                    city = user.city if user and user.city else "Москва"

            weather = WeatherAPI.get_weather(city, self.config.OPENWEATHER_API)
            query.edit_message_text(
                text=weather,
                reply_markup=get_weather_keyboard()
            )

        elif data.startswith("currency_"):
            currency = data.split("_")[1]
            currency_map = {
                "usd": ("USD", "RUB"),
                "eur": ("EUR", "RUB"),
                "cny": ("CNY", "RUB"),
                "try": ("TRY", "RUB")
            }
            base, target = currency_map.get(currency, ("USD", "RUB"))
            rate = CurrencyAPI.get_exchange_rate(base, target)
            query.edit_message_text(
                text=rate,
                reply_markup=get_currency_keyboard()
            )

        elif data.startswith("game_"):
            game_type = data.split("_")[1]

            if game_type == "random":
                number = random.randint(1, 100)
                query.edit_message_text(
                    f"🎲 Случайное число: {number}",
                    reply_markup=get_games_keyboard()
                )

            elif game_type == "guess":
                context.user_data['secret_number'] = random.randint(1, 100)
                query.edit_message_text(
                    "🎯 Я загадал число от 1 до 100!\n"
                    "Попробуйте угадать, отправив число в чат.",
                    reply_markup=get_games_keyboard()
                )
                context.user_data['playing_guess'] = True

        elif data == "back":
            query.edit_message_text(
                "Главное меню",
                reply_markup=None
            )

        elif data == "set_lang":
            query.edit_message_text(
                "Выберите язык:\n"
                "🇷🇺 Русский\n"
                "🇺🇸 English\n"
                "🇩🇪 Deutsch",
                reply_markup=get_settings_keyboard()
            )

    def error_handler(self, update: Update, context: CallbackContext):
        """Обработчик ошибок"""
        logger.error(f"Ошибка: {context.error}")
        if update and update.effective_message:
            update.effective_message.reply_text(
                "Произошла ошибка. Пожалуйста, попробуйте позже."
            )

    def run_polling(self):
        """Запуск бота в режиме polling"""
        self.updater.start_polling()
        logger.info("Бот запущен в режиме polling...")
        self.updater.idle()

    def run_webhook(self):
        """Запуск бота в режиме webhook"""
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 8443)),
            url_path=self.config.BOT_TOKEN,
            webhook_url=f"{self.config.WEBHOOK_URL}/{self.config.BOT_TOKEN}"
        )
        logger.info("Бот запущен в режиме webhook...")
        self.updater.idle()


def main():
    """Основная функция"""
    # Инициализация базы данных
    init_db()

    # Проверка токена
    if not config.Config.BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в .env файле!")
        print("Создайте .env файл с содержимым:")
        print("BOT_TOKEN=ваш_токен_от_BotFather")
        print("ADMIN_ID=ваш_telegram_id")
        return

    # Создание и запуск бота
    bot = TelegramBot(config.Config.BOT_TOKEN)

    # Выбор режима запуска
    mode = input("Выберите режим запуска (polling/webhook): ").strip().lower()

    if mode == "webhook":
        bot.run_webhook()
    else:
        bot.run_polling()


if __name__ == "__main__":
    main()