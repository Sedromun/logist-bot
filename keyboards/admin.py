from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CITIES, ROLE_NAMES



def get_choose_role_name_keyboard(id: int):
    builder = InlineKeyboardBuilder()
    for role_name_ru, role_name_en in ROLE_NAMES.items():
        builder.button(text=role_name_ru, callback_data=ChooseRoleNameCallbackFactory(text=role_name_en, id=id))
    builder.adjust(1)
    return builder.as_markup()


class ChooseRoleNameCallbackFactory(CallbackData, prefix="role_name"):
    text: str
    id: int


def get_choose_city_keyboard(id: int):
    builder = InlineKeyboardBuilder()
    for city, city_id in CITIES.items():
        builder.button(text=city, callback_data=ChooseCityCallbackFactory(city_id=city_id, id=id))
    builder.adjust(1)
    return builder.as_markup()


class ChooseCityCallbackFactory(CallbackData, prefix="city"):
    city_id: int
    id: int
