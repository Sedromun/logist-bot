from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def build_choose_rc_keyboard(rc_results, selection, rc_plan_dates):
    keyboard = []
    weekdays = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
    for i, (rc, text) in enumerate(rc_results):
        mark = "✅" if selection[rc] else "❌"
        plan_date = rc_plan_dates[rc]
        plan_date_str = plan_date.strftime("%d.%m")
        weekday_str = weekdays[plan_date.weekday()]
        # Убираем 'АО "Тандер"' из начала названия РЦ
        rc_clean = rc.strip()
        if rc_clean.startswith('АО "Тандер"'):
            rc_clean = rc_clean.replace('АО "Тандер"', '', 1).strip()
        # Формируем текст кнопки без 'АО "Тандер"'
        if "оптимальное" in text:
            qty = text.split("оптимальное")[1].strip().split()[0]
            button_text = f"{rc_clean}: оптимальное {qty} {mark} на {plan_date_str} ({weekday_str})"
        elif "(сгорит" in text:
            parts = text.split(":", 1)[1].strip()
            qty = parts.split()[0]
            burn = parts.split("(сгорит")[1].split(")")[0].strip()
            button_text = f"{rc_clean}: {qty} (сгорит {burn}) {mark} на {plan_date_str} ({weekday_str})"
        else:
            button_text = f"{text} {mark} на {plan_date_str} ({weekday_str})"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"toggle|{i}")])

    keyboard.append([InlineKeyboardButton(text=f"Сформировать запрос", callback_data="submit")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)




def build_choose_partners_keyboard(rc_results, selection):
    keyboard = []
    for i, (rc, text) in enumerate(rc_results):
        mark = "✅" if selection[rc] else "❌"
        button_text = text + mark
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"gogle|{i}")])

    keyboard.append([InlineKeyboardButton(text=f"Рассылка партнерам", callback_data="sub_part")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def partners_agreement_keyboard(shipment_id: int = None):
    keyboard = []
    keyboard.append([InlineKeyboardButton(text=f"✅ Принять", callback_data=f"accept|{shipment_id}")])
    keyboard.append([InlineKeyboardButton(text=f"❌ Откааться", callback_data=f"dismiss|{shipment_id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)