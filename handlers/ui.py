
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🧩 Онбординг"), KeyboardButton("🧑‍💼 Вопрос HR"))
    kb.add(KeyboardButton("🏢 О компании"), KeyboardButton("⭐ Миссия и ценности"))
    kb.add(KeyboardButton("📍 Филиал"), KeyboardButton("🛡️ Безопасность"))
    kb.add(KeyboardButton("👩‍💼 HR"), KeyboardButton("💰 Льготы"))
    kb.add(KeyboardButton("🏅 Спорт и жизнь"), KeyboardButton("👥 Профсоюз"))
    kb.add(KeyboardButton("🧾 Этика"), KeyboardButton("📣 Коммуникации"))
    kb.add(KeyboardButton("🧑‍💻 ИТ"), KeyboardButton("🆘 Помощь"))
    return kb

def onboarding_keyboard():
    ik = InlineKeyboardMarkup()
    steps = [
        ("1) Приветствие директора", "onb:welcome"),
        ("2) О компании", "onb:company"),
        ("3) Безопасность", "onb:safety"),
        ("4) HR и обучение", "onb:hr"),
        ("5) Льготы", "onb:benefits"),
        ("6) ИТ и сервисы", "onb:it"),
        ("7) Этика и коммуникации", "onb:ethics"),
    ]
    for t, cb in steps:
        ik.add(InlineKeyboardButton(t, callback_data=cb))
    return ik

def section_actions(section_id: str):
    ik = InlineKeyboardMarkup()
    ik.add(InlineKeyboardButton("📖 Подробнее", callback_data=f"sec:{section_id}:long"))
    ik.add(InlineKeyboardButton("❓ Все вопросы", callback_data=f"sec:{section_id}:faq"))
    return ik
