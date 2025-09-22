from asyncio.log import logger
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject, StateFilter

from aiogram.enums import ContentType
from aiogram import F, Router

from database.controllers.role import create_role, update_role
from database.controllers.users import register_user, update_user
from utils.register import check_code


register_router = Router(name="register")

@register_router.message(StateFilter(None), Command("start"))
async def start_handler(message: Message, command: CommandObject):
    logger.info("start_handler")
    await message.answer("Введите код для регистрации, который вам выдали")


@register_router.message()
async def register_handler(message: Message):
    res = check_code(message.text)
    if res == "admin":
        register_user(message.from_user.id)
        role = create_role()
        logger.info(role)
        update_role(role.id, {"role_name": "admin", "is_admin": True, "user_id": message.from_user.id})
        await message.answer("Админ - успешно зарегестрирован")
    elif res == None:
        await message.answer("Некорретная команда или код введен неверно")
    else:
        user = register_user(message.from_user.id)
        update_role(res.id, {"user_id": message.from_user.id})
        await message.answer(f"Успешная регистрация:\nРоль : {res.role_name}\nГород : {res.city}")

