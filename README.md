# Telegram Quiz Bot

Бот проводит викторину с 10 вопросами и показывает статистику.

## Команды бота

- `/start` — запуск бота
- `/quiz` — начать викторину
- `/exit` — выйти из викторины
- `/stats` — показать статистику

## Ссылка на бота

[@quuu1zzz_bot](https://t.me/quuu1zzz_bot)

## Запуск своего бота

1. Клонируйте репозиторий.
2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
```
3. Создайте .env файл на основе .env.example.
4. Перейдите в директорию
```bash
cd bot
```
6. Запустите бота:
```bash
python main.py
```