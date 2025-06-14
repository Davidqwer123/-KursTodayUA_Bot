from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from services.api_client import get_exchange_rates

router = Router()


class ConvertCurrency(StatesGroup):
    waiting_for_amount = State()
    waiting_for_currency = State()


@router.message(Command("convert"))
async def cmd_convert(message: Message, state: FSMContext):
    await message.answer(
        "Введіть суму для конвертації:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ConvertCurrency.waiting_for_amount)


@router.message(ConvertCurrency.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Будь ласка, введіть коректну суму (число більше 0)")
        return

    await state.update_data(amount=amount)

    rates = get_exchange_rates()
    if not rates:
        await message.answer("Не вдалося отримати курс валют. Спробуйте пізніше.")
        await state.clear()
        return

    # Виправлено створення клавіатури
    buttons = [[KeyboardButton(text=rate['ccy'])] for rate in rates]
    buttons.append([KeyboardButton(text="Скасувати")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

    await message.answer("Оберіть валюту:", reply_markup=keyboard)
    await state.set_state(ConvertCurrency.waiting_for_currency)


@router.message(ConvertCurrency.waiting_for_currency)
async def process_currency(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        await message.answer("Конвертацію скасовано", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    data = await state.get_data()
    amount = data['amount']

    rates = get_exchange_rates()
    selected_rate = next((rate for rate in rates if rate['ccy'] == message.text), None)

    if not selected_rate:
        await message.answer("Оберіть валюту зі списку")
        return

    converted_amount = amount * float(selected_rate['buy'])
    response = (
        f"{amount} {selected_rate['ccy']} = {converted_amount:.2f} {selected_rate['base_ccy']}\n"
        f"Курс: 1 {selected_rate['ccy']} = {selected_rate['buy']} {selected_rate['base_ccy']}"
    )

    await message.answer(response, reply_markup=ReplyKeyboardRemove())
    await state.clear()