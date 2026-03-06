
# TPLUS HR BOT — IDEAL V2

## Почему V2
- исправлены кнопки и маршрутизация (один диспетчер вместо нескольких "catch-all")
- бот отвечает на вопросы по блокам и умеет подсказать похожие FAQ
- расширенная база Q&A по презентации

## Запуск на macOS (PEP 668)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Вставьте токен в `config.py` и запустите:
```bash
python bot.py
```

## Основные кнопки
- 🧩 Онбординг — пошаговый маршрут новичка
- Темы (Компания/Безопасность/HR/Льготы/ИТ/Этика/Коммуникации/Профсоюз/Спорт)
- 🧑‍💼 Вопрос HR — сбор деталей и готовый текст обращения

## Docker (быстрый запуск)

### Вариант A — docker-compose (рекомендую)
1) Создайте файл `.env` рядом с `docker-compose.yml`:
```
TOKEN=ваш_токен_бота
```
2) Запуск:
```
docker compose up -d --build
```
3) Логи:
```
docker compose logs -f
```

### Вариант B — чистый Docker
```
docker build -t tplus-hr-bot .
docker run -d --name tplus-hr-bot --restart unless-stopped -e TOKEN=ваш_токен_бота tplus-hr-bot
```
# tgbot_for_forum
