import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import load_settings
from handlers import common, order


async def main() -> None:
    settings = load_settings()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Поддержка прокси через переменные окружения (подходит для VPN/прокси на Windows):
    # - HTTPS_PROXY / HTTP_PROXY
    # - ALL_PROXY (на всякий случай)
    proxy_url = (
        (os.getenv("HTTPS_PROXY") or "").strip()
        or (os.getenv("HTTP_PROXY") or "").strip()
        or (os.getenv("ALL_PROXY") or "").strip()
        or None
    )

    # В aiogram 3.x можно передать AiohttpSession с proxy.
    session = AiohttpSession(proxy=proxy_url) if proxy_url else AiohttpSession()
    bot = Bot(token=settings.bot_token, session=session)
    dp = Dispatcher(storage=MemoryStorage())

    # Прокидываем настройки в DI-контекст aiogram, чтобы их можно было получать параметром settings: Settings
    dp.workflow_data.update(settings=settings)

    dp.include_router(order.router)
    dp.include_router(common.router)

    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Оставить заявку"),
                BotCommand(command="help", description="Контакты и справка"),
                BotCommand(command="cancel", description="Отменить заявку"),
            ]
        )

        await dp.start_polling(bot)
    except TelegramNetworkError as e:
        # Самая частая проблема: Telegram API недоступен из-за сети/провайдера/блокировок.
        msg = "\n".join(
            [
                "Не удалось подключиться к Telegram API (api.telegram.org).",
                "",
                f"Текст ошибки: {e}",
                "",
                "Что сделать:",
                "- Проверьте интернет (иногда помогает раздать с телефона).",
                "- Если Telegram у провайдера ограничен — включите VPN/прокси.",
                "- Если используете прокси, задайте HTTPS_PROXY или HTTP_PROXY в окружении.",
                "",
                "Пример для PowerShell (до запуска):",
                '  $env:HTTPS_PROXY="http://127.0.0.1:1080"',
                "  python main.py",
            ]
        )
        print(msg)
        raise
    finally:
        # Закрываем HTTP-сессию корректно, чтобы не было Unclosed client session
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

