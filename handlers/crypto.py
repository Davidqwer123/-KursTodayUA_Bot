from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.api_client import BinanceAPI

# Створюємо роутер для криптовалютних команд
crypto_router = Router()


@crypto_router.message(Command("crypto_convert"))
async def crypto_rates(message: types.Message):
    """Показати курси BTC, ETH, USDT"""
    btc_price = BinanceAPI.get_crypto_price("BTCUSDT")
    eth_price = BinanceAPI.get_crypto_price("ETHUSDT")

    text = (
        f"💰 <b>Курси криптовалют:</b>\n\n"
        f"🟠 <b>BTC:</b> ${btc_price:,.2f}\n"
        f"🔵 <b>ETH:</b> ${eth_price:,.2f}"
    )

    await message.answer(text, parse_mode="HTML")


@crypto_router.message(Command("convertе"))
async def crypto_convert(message: types.Message):
    """Конвертація криптовалют (/converte 0.01 BTC to USDT)"""
    try:
        args = message.text.split()
        amount = float(args[1])
        from_asset = args[2].upper()
        to_asset = args[4].upper()

        result = BinanceAPI.convert_crypto(amount, from_asset, to_asset)
        await message.answer(f"🔹 {amount} {from_asset} = {result:.8f} {to_asset}")
    except (IndexError, ValueError):
        await message.answer("❌ Використовуйте: <code>/convert 0.01 BTC to USDT</code>", parse_mode="HTML")


@crypto_router.message(Command("convert_to_uah"))
async def convert_to_uah_handler(message: types.Message):
    """Конвертувати крипту в гривні (/convert_to_uah 0.01 BTC)"""
    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError

        amount = float(args[1])
        crypto = args[2].upper()

        if crypto not in ["BTC", "ETH"]:
            await message.answer("❌ Підтримуються лише BTC та ETH")
            return

        result = BinanceAPI.convert_to_uah(amount, crypto)
        await message.answer(f"🔹 {amount} {crypto} = {result:,.2f} ₴")

    except ValueError:
        await message.answer("❌ Невірний формат. Використовуйте: /convert_to_uah 0.01 BTC")


def get_crypto_router() -> Router:
    """Створює та повертає роутер для криптовалютних операцій"""
    crypto_router = Router()

    # Клавіатура для швидкої конвертації
    def get_conversion_keyboard():
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="BTC → UAH",
                callback_data="convert_btc_uah"
            ),
            types.InlineKeyboardButton(
                text="ETH → UAH",
                callback_data="convert_eth_uah"
            )
        )
        return builder.as_markup()

    @crypto_router.message(Command("crypto_rates"))
    async def show_crypto_rates(message: types.Message):
        """Показує курси криптовалют з кнопками"""
        btc_rate = BinanceAPI.get_crypto_to_uah("BTC")
        eth_rate = BinanceAPI.get_crypto_to_uah("ETH")

        text = (
            f"📊 <b>Поточні курси:</b>\n\n"
            f"🟠 1 BTC = {btc_rate:,.2f} ₴\n"
            f"🔵 1 ETH = {eth_rate:,.2f} ₴\n\n"
            f"Оберіть пару для конвертації:"
        )

        await message.answer(
            text,
            reply_markup=get_conversion_keyboard(),
            parse_mode="HTML"
        )

    @crypto_router.message(Command("convert_to_uah"))
    async def convert_to_uah(message: types.Message):
        """Обробляє команду конвертації (/convert_to_uah 0.1 BTC)"""
        try:
            args = message.text.split()
            if len(args) != 3:
                raise ValueError

            amount = float(args[1])
            crypto = args[2].upper()

            if crypto not in ["BTC", "ETH"]:
                await message.answer("❌ Підтримуються лише BTC та ETH")
                return

            result = BinanceAPI.convert_to_uah(amount, crypto)
            await message.answer(f"🔹 {amount} {crypto} = {result:,.2f} ₴")

        except ValueError:
            await message.answer(
                "❌ Невірний формат. Використовуйте:\n"
                "<code>/convert_to_uah [кількість] [BTC/ETH]</code>",
                parse_mode="HTML"
            )

    @crypto_router.callback_query(lambda c: c.data.startswith("convert_"))
    async def handle_conversion(callback: types.CallbackQuery):
        """Обробляє кнопки швидкої конвертації"""
        try:
            _, crypto, currency = callback.data.split("_")
            amount = 1  # Конвертуємо 1 одиницю за замовчуванням

            if crypto == "btc":
                result = BinanceAPI.convert_to_uah(amount, "BTC")
                text = f"🟠 1 BTC = {result:,.2f} ₴"
            elif crypto == "eth":
                result = BinanceAPI.convert_to_uah(amount, "ETH")
                text = f"🔵 1 ETH = {result:,.2f} ₴"
            else:
                raise ValueError

            await callback.message.edit_text(text)
            await callback.answer()

        except Exception as e:
            await callback.answer("❌ Помилка конвертації", show_alert=True)

    return crypto_router