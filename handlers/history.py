from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from services.api_client import get_historical_rates
from services.chart_service import create_usd_chart

router = Router()


@router.message(Command('usd_history'))
async def usd_history_handler(message: Message):
    try:
        dates, rates = get_historical_rates()

        if not rates or len(rates) < 2:
            await message.answer('Недостатньо даних для побудови графіка')
            return

        # Отримуємо графік у вигляді байтів
        chart_buf = create_usd_chart(dates, rates)

        # Створюємо файл, який aiogram може надіслати
        chart_file = BufferedInputFile(
            chart_buf.getvalue(), filename="usd_history.png"
        )

        # Відправляємо зображення
        await message.answer_photo(photo=chart_file)

        # Формуємо текстовий опис
        UA_MONTHS = {
            1: "січ",
            2: "лют",
            3: "бер",
            4: "квіт",
            5: "трав",
            6: "черв",
            7: "лип",
            8: "серп",
            9: "вер",
            10: "жовт",
            11: "лист",
            12: "груд",
        }

        history_text = "📊 Курс USD/UAH за останні 7 днів:\n\n"
        for date, rate in zip(dates, rates):
            day = date.day
            month = UA_MONTHS[date.month]
            year = date.year
            history_text += f"• {day:02d} {month} {year}: <b>{rate:.2f}</b> грн\n"

        await message.answer(history_text, parse_mode='HTML')

    except Exception as e:
        await message.answer(f'⚠️ Сталася помилка: {str(e)}')
        raise
