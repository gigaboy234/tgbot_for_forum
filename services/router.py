
import json
from typing import Optional

with open("data/routing.json", encoding="utf-8") as f:
    ROUTING = json.load(f)

BUTTON_MAP = {
    "🏢 О компании":"company",
    "⭐ Миссия и ценности":"values",
    "📍 Филиал":"branch",
    "🛡️ Безопасность":"safety",
    "📣 Коммуникации":"comms",
    "👩‍💼 HR":"hr",
    "🏅 Спорт и жизнь":"sports_culture",
    "💰 Льготы":"benefits",
    "👥 Профсоюз":"union",
    "🧾 Этика":"ethics",
    "🧑‍💻 ИТ":"it",
    "👋 Приветствие":"welcome",
}

def route(text: str) -> Optional[str]:
    if not text:
        return None
    t = text.strip().lower()

    # buttons
    for b, sid in BUTTON_MAP.items():
        if t == b.lower():
            return sid

    # keyword routing
    for sid, keys in ROUTING.items():
        for k in keys:
            if k in t:
                return sid
    return None
