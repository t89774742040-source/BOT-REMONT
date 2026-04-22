from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


_BANNED_PATTERNS = [
    r"\bтв\b",
    r"\btv\b",
    r"телевиз",
    r"холодил",
]


def contains_banned_words(text: str) -> bool:
    """
    Если пользователь просит ремонт ТВ/холодильника — сразу вежливо отказываем.
    """
    t = (text or "").lower()
    return any(re.search(p, t) for p in _BANNED_PATTERNS)


def normalize_phone(raw: str) -> str | None:
    """
    Валидация телефона:
    - принимаем +7XXXXXXXXXX или 8XXXXXXXXXX или просто 11 цифр
    - на выходе возвращаем нормализованное +7XXXXXXXXXX
    """
    if not raw:
        return None

    digits = re.sub(r"\D+", "", raw)
    if len(digits) != 11:
        return None

    if digits.startswith("8"):
        digits = "7" + digits[1:]
    if not digits.startswith("7"):
        return None

    return f"+{digits}"


def now_msk_str() -> str:
    # Без внешних библиотек: фиксируем время в UTC, мастер увидит по своему часовому поясу в Telegram.
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def append_request_log(text: str) -> None:
    """
    Дублируем заявку в лог-файл. Это удобно, если Telegram “потерял” сообщение.
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "requests.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n" + ("-" * 40) + "\n")

