from asyncio.log import logger
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject, StateFilter

from aiogram.enums import ContentType
from aiogram import F, Router

from config import ID_TO_CITY_NAME
from database.controllers.role import create_role, update_role
from keyboards.admin import ChooseCityCallbackFactory, ChooseRoleNameCallbackFactory, get_choose_city_keyboard, get_choose_role_name_keyboard
from middlewares.base import AccessMiddleware
from utils.register import encrypt_code


admin_router = Router(name="admin")

admin_router.message.middleware(AccessMiddleware(role="admin"))

@admin_router.message(StateFilter(None), Command("create_role"))
async def admin_create_role_handler(message: Message, command: CommandObject):
    logger.info(f"Message: '{message.message_id}' - admin.admin_create_role_handler")
    role = create_role()
    await message.answer(text="Чтобы создать юзера выберите роль:", reply_markup=get_choose_role_name_keyboard(role.id))


@admin_router.callback_query(ChooseRoleNameCallbackFactory.filter())
async def choose_role_callback(
    callback: CallbackQuery, callback_data: ChooseRoleNameCallbackFactory
):
    logger.info(f"Callback: '{callback.id}' - admin.choose_role_callback")
    role_id = callback_data.id

    update_role(role_id, {"role_name": callback_data.text})
    await callback.message.edit_text(text="Выберите город", reply_markup=get_choose_city_keyboard(id=role_id))
    await callback.answer()

@admin_router.callback_query(ChooseCityCallbackFactory.filter())
async def choose_city_callback(
    callback: CallbackQuery, callback_data: ChooseCityCallbackFactory
):
    logger.info(f"Callback: '{callback.id}' - admin.choose_city_callback")
    role_id = callback_data.id
    code = encrypt_code(role_id)
    update_role(role_id, {"city": ID_TO_CITY_NAME[callback_data.city_id], "code": code})
    await callback.message.edit_text(
        text=f"Новый юзер успешно создан!\nОтправьте ему код для доступа к боту:\n\n<code>{code}</code>"
    )
    await callback.answer()




