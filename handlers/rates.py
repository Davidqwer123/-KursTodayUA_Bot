# handlers/rates.py
from aiogram import Router, types
from aiogram.filters import Command
from services.api_client import get_all_bank_rates

from services.api_client import get_exchange_rates

# Створюємо роутер для цього модуля
router = Router()
@router.message(Command("rates"))
async def cmd_rates(message: types.Message):
    rates = get_all_bank_rates()
    if not rates:
        await message.answer("❌ Не вдалося отримати курс валют. Спробуйте пізніше.")
        return

    response = "<b>💱 Поточні курси валют:</b>\n\n"

    for bank_name, bank_rates in rates.items():
        response += f"<b>🏦 {bank_name}</b>\n"
        for rate in bank_rates:
            response += (
                f"🔸 <b>{rate['ccy']} → {rate['base_ccy']}</b>\n"
                f"🟢 Купівля: <code>{rate['buy']}</code>\n"
                f"🔴 Продаж: <code>{rate['sale']}</code>\n\n"
            )

    await message.answer(response, parse_mode="HTML")
# @router.message(Command("rates"))
# async def cmd_rates(message: types.Message):
#     rates = get_exchange_rates()
#     if not rates:
#         await message.answer("Не вдалося отримати курс валют. Спробуйте пізніше.")
#         return
#
#     response = "💵 Поточний курс:\n\n"
#     for rate in rates:
#         response += (
#             f"{rate['ccy']} → {rate['base_ccy']}:\n"
#             f"Купівля: {rate['buy']}\n"
#             f"Продаж: {rate['sale']}\n\n"
#         )
#     await message.answer(response)


# Реєстрація роутера в головному Dispatcher
def register_rates_handlers(dp):
    dp.include_router(router)
