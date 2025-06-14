from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.rates import router as rates_router
from handlers.convert import router as convert_router
from handlers.history import router as history_router
from handlers.crypto import crypto_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(rates_router)
    dp.include_router(convert_router)
    dp.include_router(history_router)
    dp.include_router(crypto_router)




    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
