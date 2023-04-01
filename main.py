import asyncio
from aiogram import Bot, Dispatcher
from handlers import handler_users, handler_admin
import config
bot_token = config.bot_token


bot = Bot(token=bot_token)


async def main():
    dp = Dispatcher()
    dp.include_router(handler_users.router)
    dp.include_router(handler_admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

