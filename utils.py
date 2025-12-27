import requests
import json
from datetime import datetime, timedelta
import random


class WeatherAPI:
    @staticmethod
    def get_weather(city, api_key):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("cod") != 200:
                return f"Город '{city}' не найден"

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            description = data["weather"][0]["description"].capitalize()
            city_name = data["name"]

            return (f"🌤️ Погода в {city_name}:\n"
                    f"🌡️ Температура: {temp}°C\n"
                    f"🤔 Ощущается как: {feels_like}°C\n"
                    f"💧 Влажность: {humidity}%\n"
                    f"💨 Ветер: {wind} м/с\n"
                    f"☁️ {description}")
        except:
            return "Ошибка получения данных о погоде"


class CurrencyAPI:
    @staticmethod
    def get_exchange_rate(base="USD", target="RUB"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = requests.get(url, timeout=10)
            data = response.json()
            rate = data["rates"][target]
            return f"💱 {base}/{target}: {rate:.2f}"
        except:
            return "Ошибка получения курса валют"


class JokesAPI:
    jokes = [
        "Почему программисты путают Хэллоуин и Рождество?\nПотому что 31 OCT = 25 DEC.",
        "Сколько программистов нужно, чтобы вкрутить лампочку?\nНи одного. Это проблема на стороне железа.",
        "Программист звонит в библиотеку:\n— Здравствуйте, есть книга «Как решить все проблемы»?\n— Книга есть, но она не помогает...",
        "Почему Python не идет в спортзал?\nПотому что он боится потерять свои скобки!",
        "Что сказал один бит другому?\nДавай встретимся на шоссе!"
    ]

    @staticmethod
    def get_random_joke():
        return random.choice(JokesAPI.jokes)


class Calculator:
    @staticmethod
    def calculate(expression):
        try:
            # Безопасный eval
            allowed_chars = "0123456789+-*/(). "
            if any(char not in allowed_chars for char in expression):
                return "Недопустимые символы в выражении"

            result = eval(expression)
            return f"✅ Результат: {result}"
        except ZeroDivisionError:
            return "❌ Ошибка: деление на ноль"
        except:
            return "❌ Ошибка в выражении"


class NewsAPI:
    @staticmethod
    def get_news():
        try:
            url = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=ВАШ_API_KEY"
            response = requests.get(url)
            data = response.json()

            articles = data.get("articles", [])[:5]
            news_text = "📰 Последние новости:\n\n"

            for i, article in enumerate(articles, 1):
                title = article.get("title", "Без заголовка")
                news_text += f"{i}. {title}\n"

            return news_text
        except:
            return "Новости временно недоступны"