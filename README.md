## Telegram-бот для мастерской (aiogram 3.x)

Rule-based бот без нейросетей и без внешних API. Сценарий — FSM на **4 шага** с инлайн-кнопками и валидацией телефона. Готовую заявку бот пересылает мастеру в чат `ADMIN_ID` и дублирует в `logs/requests.log`.

### Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Настройка

- Скопируйте `.env.example` в `.env`
- Заполните `BOT_TOKEN` и `ADMIN_ID` (и при желании остальные поля)

### Запуск

```bash
python main.py
```

### Команды

- `/start` — начать оформление заявки
- `/help` — контакты и справка
- `/cancel` — отменить и сбросить заявку

