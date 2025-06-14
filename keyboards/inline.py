from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_currency_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("USD", callback_data="currency_USD"),
        types.InlineKeyboardButton("EUR", callback_data="currency_EUR"),
        types.InlineKeyboardButton("RUR", callback_data="currency_RUR")
    )
    return keyboard




def crypto_keyboard():
    """Клавіатура для швидкої конвертації"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("BTC → USDT", callback_data="convert_btc_usdt"),
        InlineKeyboardButton("USDT → BTC", callback_data="convert_usdt_btc"),
    )
    return keyboard