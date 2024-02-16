import asyncio

from aiogram import Dispatcher

from bot.config import bot
from bot.handlers import user_handlers, db_handlers, edit_handlers, content_handlers


async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(user_handlers.router, db_handlers.router, edit_handlers.router, content_handlers.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except:
        print("there is an exception")


if __name__ == "__main__":
    asyncio.run(main())
