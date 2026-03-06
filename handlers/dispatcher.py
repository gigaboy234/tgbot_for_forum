
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.store import get as get_user, set as set_user
from services.router import route, BUTTON_MAP
from services.kb import get_section
from services.search import search
from handlers.ui import main_menu, onboarding_keyboard, section_actions

HELP_TEXT = (
    "Я умею:\n"
    "• провести онбординг (кнопка «🧩 Онбординг»)\n"
    "• отвечать на вопросы по темам из презентации\n"
    "• подобрать похожий вопрос, если вы написали своими словами\n"
    "• собрать обращение в HR (кнопка «🧑‍💼 Вопрос HR»)\n\n"
    "Попробуйте написать, например:\n"
    "— «Какие льготы?»\n"
    "— «Что делать, если написал журналист?»\n"
    "— «Как обратиться на горячую линию?»"
)

def _topic_card(section):
    text = f"{section['title']}\n\n{section['summary']}\n\n📌 Частые вопросы:\n"
    for i, item in enumerate(section.get("faqs", [])[:7], 1):
        text += f"{i}. {item['q']}\n"
    text += "\nНапишите вопрос своими словами — я отвечу."
    return text

def register(bot):

    @bot.message_handler(commands=["start"])
    def start(m):
        u = get_user(m.from_user.id)
        if not u.get("name"):
            set_user(m.from_user.id, {"state":"ask_name"})
            bot.send_message(m.chat.id, "Привет! 👋 Как к вам можно обращаться? Напишите имя.")
            return
        bot.send_message(m.chat.id, f"Привет, {u['name']}! Выберите тему или задайте вопрос.", reply_markup=main_menu())

    @bot.callback_query_handler(func=lambda c: c.data.startswith("onb:"))
    def onb(c):
        sid = c.data.split(":",1)[1]
        section = get_section(sid)
        if not section:
            bot.answer_callback_query(c.id, "Шаг не найден")
            return
        bot.send_message(c.message.chat.id, f"{section['title']}\n\n{section['long']}")
        bot.answer_callback_query(c.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("sec:"))
    def sec(c):
        _, sid, action = c.data.split(":",2)
        section = get_section(sid)
        if not section:
            bot.answer_callback_query(c.id, "Раздел не найден")
            return

        if action == "long":
            bot.send_message(c.message.chat.id, f"{section['title']}\n\n{section['long']}")
        elif action == "faq":
            text = f"{section['title']}\n\n"
            for i, it in enumerate(section.get("faqs", []), 1):
                text += f"{i}) {it['q']}\n— {it['a']}\n\n"
            bot.send_message(c.message.chat.id, text[:4000])
        bot.answer_callback_query(c.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("pick:"))
    def pick(c):
        # pick answer from suggestions
        _, sid, idx = c.data.split(":")
        section = get_section(sid)
        i = int(idx)
        faqs = section.get("faqs", [])
        if 0 <= i < len(faqs):
            bot.send_message(c.message.chat.id, f"✅ {faqs[i]['a']}")
        bot.answer_callback_query(c.id)

    @bot.message_handler(func=lambda m: True)
    def handle(m):
        text = (m.text or "").strip()
        u = get_user(m.from_user.id)

        # 1) name capture
        if u.get("state") == "ask_name":
            if len(text) < 2:
                bot.send_message(m.chat.id, "Напишите имя чуть понятнее 🙂")
                return
            set_user(m.from_user.id, {"name": text, "state":"ready"})
            # director greeting
            section = get_section("welcome")
            bot.send_message(
                m.chat.id,
                f"Рад знакомству, {text}! 👋\n\n{section['long']}\n\n"
                "Дальше — быстрый онбординг или выберите тему:",
                reply_markup=main_menu()
            )
            return

        # 2) buttons
        if text == "🆘 Помощь":
            bot.send_message(m.chat.id, HELP_TEXT, reply_markup=main_menu())
            return

        if text == "🧩 Онбординг":
            bot.send_message(m.chat.id, "Онбординг (5 минут). Выберите шаг:", reply_markup=onboarding_keyboard())
            return

        # HR flow
        if text == "🧑‍💼 Вопрос HR":
            set_user(m.from_user.id, {"state":"hr_q"})
            bot.send_message(m.chat.id, "Опишите вопрос одним сообщением. Я уточню детали и подготовлю обращение.")
            return

        if u.get("state") == "hr_q":
            if len(text) < 8:
                bot.send_message(m.chat.id, "Сформулируйте чуть подробнее 🙂")
                return
            set_user(m.from_user.id, {"state":"hr_details", "hr_question": text})
            bot.send_message(
                m.chat.id,
                "Уточните, пожалуйста:\n"
                "1) Город/площадка\n"
                "2) Срочность (сегодня/на неделе/не срочно)\n"
                "3) Контакт (почта/телефон) — если можно"
            )
            return

        if u.get("state") == "hr_details":
            q = u.get("hr_question","")
            details = text
            set_user(m.from_user.id, {"state":"ready"})
            bot.send_message(
                m.chat.id,
                "Готово ✅ Ниже текст обращения (скопируйте в HR-канал/почту):\n\n"
                f"— Вопрос: {q}\n"
                f"— Детали: {details}\n"
                f"— От: {m.from_user.first_name} (@{m.from_user.username or '—'})\n"
            )
            return

        # open topic if routed by button or keywords
        sid = route(text)
        if sid:
            section = get_section(sid)
            if section:
                bot.send_message(m.chat.id, _topic_card(section), reply_markup=section_actions(sid))
                return

        # 3) free text search
        hits = search(text, limit=4)
        if not hits:
            bot.send_message(
                m.chat.id,
                "Я не нашёл точного ответа в базе презентации.\n"
                "Нажмите «🧑‍💼 Вопрос HR», и я соберу детали, чтобы HR ответили быстро.",
                reply_markup=main_menu()
            )
            return

        best = hits[0]
        # if high confidence — answer directly
        if best["score"] >= 0.70:
            bot.send_message(m.chat.id, f"✅ {best['a']}")
            return

        # otherwise show suggestions
        msg = "Я нашёл похожие вопросы. Выберите вариант:\n\n"
        ik = InlineKeyboardMarkup()
        for h in hits:
            sec = get_section(h["section_id"])
            # find index in section faqs
            idx = 0
            for i, it in enumerate(sec.get("faqs", [])):
                if it["q"] == h["q"]:
                    idx = i
                    break
            msg += f"• {h['q']} ({h['section_title']})\n"
            ik.add(InlineKeyboardButton(h["q"][:60], callback_data=f"pick:{h['section_id']}:{idx}"))
        bot.send_message(m.chat.id, msg, reply_markup=ik)
