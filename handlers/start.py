from aiogram import Router, types
from aiogram.filters import Command

router = Router()                          # ← створюємо роутер

@router.message(Command(commands=["start", "help"]))
async def cmd_start(message: types.Message):
    """
    Обробляє /start та /help.
    """
    await message.answer(
        text=f'Привіт, @{message.chat.username}!\n'
        "Я бот валют.\n"
        "/rates – поточний курс\n"
        "/convert – конвертація суми\n"
        "/usd_history – історія курсу за 7 днів\n"
        "/crypto_convert - крипто конвертація"
        # Додано нову команду
    )

# Функція, яку викликаємо у main.py
def register_start_handlers(dp):
    dp.include_router(router)