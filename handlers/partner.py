from asyncio.log import logger
import os
import datetime
import pandas as pd
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram import F, Router
import asyncio
import openpyxl
import pandas as pd
from aiogram.types import FSInputFile
from database.controllers.shipment import create_shipment, get_shipment, update_shipment
from database.controllers.users import get_user
from utils.basic import normalize_rc_name
from utils.planner import is_green, has_green_in_last_4_days, send_messages_to_partners
from keyboards.planner import build_choose_partners_keyboard, build_choose_rc_keyboard
from config import bot, dp
from middlewares import AccessMiddleware

# Простое хранилище для выбора пользователя (user_id: {selection, results})
user_selections = {}

partner_router = Router(name="partner")

partner_router.message.middleware(AccessMiddleware(role="partner"))

@partner_router.callback_query(lambda c: c.data.startswith("accept|"))
async def accept_shipment(query: CallbackQuery):
    shipment_id = int(query.data.split("|", 1)[1])
    shipment = get_shipment(shipment_id)
    if shipment is None:
        await query.answer("Ошибка: вывоз не найден.")
        logger.error(f"Shipment with id={shipment_id} not found. City: {user.city} ({user.id})")
        return
    user = get_user(query.from_user.id)
    admin = get_user(shipment.admin_id)
    update_shipment(shipment_id, {"status": "accepted"})

    await bot.send_message(chat_id=admin.id, text=f"Партнер принял вывоз:\n {shipment._asdict()}")


    await query.message.edit_text(text="Вы успешно приняли вывоз!")
    await query.answer()


@partner_router.callback_query(lambda c: c.data.startswith("dismiss|"))
async def dismiss_shipment(query: CallbackQuery):
    shipment_id = int(query.data.split("|", 1)[1])
    shipment = get_shipment(shipment_id)
    if shipment is None:
        await query.answer("Ошибка: вывоз не найден.")
        logger.error(f"Shipment with id={shipment_id} not found. City: {user.city} ({user.id})")
        return
    user = get_user(query.from_user.id)
    admin = get_user(shipment.admin_id)

    update_shipment(shipment_id, {"status": "rejected"})

    await bot.send_message(chat_id=admin.id, text=f"Партнер отказался от вывоза:\n {shipment._asdict()}")


    await query.message.edit_text(text="Вы отказались от вывоза.")
    await query.answer()