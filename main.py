import asyncio
from config import FERNET, bot, dp
from handlers import planner_router, register_router, admin_router, partner_router, warehouse_router

dp.include_router(admin_router)
dp.include_router(planner_router)
dp.include_router(register_router)
dp.include_router(partner_router)
dp.include_router(warehouse_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())