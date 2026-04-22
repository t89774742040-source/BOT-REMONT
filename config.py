from __future__ import annotations

from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    # Основные параметры из ТЗ
    master_name: str
    master_phone: str
    address: str
    service_area: str
    diagnostic_price: int

    # Технические параметры
    bot_token: str
    admin_id: int


def load_settings() -> Settings:
    """
    Загружает конфиг из .env.
    Все значения валидируются минимально, чтобы бот падал сразу и понятно.
    """
    load_dotenv()

    bot_token = (getenv("BOT_TOKEN") or "").strip()
    if not bot_token:
        raise RuntimeError("Не задан BOT_TOKEN в .env")

    admin_id_raw = (getenv("ADMIN_ID") or "").strip()
    if not admin_id_raw:
        raise RuntimeError("Не задан ADMIN_ID в .env")
    try:
        admin_id = int(admin_id_raw)
    except ValueError as e:
        raise RuntimeError("ADMIN_ID должен быть числом (int)") from e

    master_name = (getenv("MASTER_NAME") or "Сергей").strip()
    master_phone = (getenv("MASTER_PHONE") or "+7-909-995-74-22").strip()
    address = (getenv("ADDRESS") or "г. Одинцово, район Трехгорка, ул. Кутузовская 25").strip()
    service_area = (getenv("SERVICE_AREA") or "Трехгорка, Одинцово и ближайшие посёлки (~10 км)").strip()

    diagnostic_price_raw = (getenv("DIAGNOSTIC_PRICE") or "800").strip()
    try:
        diagnostic_price = int(diagnostic_price_raw)
    except ValueError as e:
        raise RuntimeError("DIAGNOSTIC_PRICE должен быть числом (int)") from e

    return Settings(
        master_name=master_name,
        master_phone=master_phone,
        address=address,
        service_area=service_area,
        diagnostic_price=diagnostic_price,
        bot_token=bot_token,
        admin_id=admin_id,
    )

