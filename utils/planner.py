import datetime

from database.controllers.shipment import create_shipment
from database.controllers.users import get_user_by_city
from config import bot
from keyboards.planner import partners_agreement_keyboard
from utils.basic import normalize_rc_name

def is_green(cell):
    fill = cell.fill
    if fill is not None and hasattr(fill, 'fgColor') and fill.fgColor is not None:
        fgColor = fill.fgColor
        color = None
        if hasattr(fgColor, 'rgb') and fgColor.rgb is not None:
            color = fgColor.rgb
        elif hasattr(fgColor, 'type') and fgColor.type == 'rgb' and hasattr(fgColor, 'value'):
            color = fgColor.value
        if color is not None and isinstance(color, str):
            return color.upper() in ['FF92D050', '92D050']
    return False

def has_green_in_last_4_days(ws, row_idx, date_cols, plan_date):
    # Берём 4 дня до планируемого: plan_date-1, plan_date-2, plan_date-3, plan_date-4
    days = [plan_date - datetime.timedelta(days=i) for i in range(1, 5)]
    header_row = 4  # pandas header=3, значит названия колонок в 4-й строке (индекс 4 для openpyxl)
    header_values = [cell.value for cell in ws[header_row]]
    col_indices = []
    for day in days:
        for col, date in date_cols:
            if date.date() == day:
                if col in header_values:
                    col_indices.append(header_values.index(col) + 1)
                break
    excel_row = row_idx + 5
    for col_idx in col_indices:
        cell = ws.cell(row=excel_row, column=col_idx)
        if is_green(cell):
            return True
    return False


async def send_messages_to_partners(filtered, admin_id: int):
    none_cities = []
    success_cities = []
    for (rc, text) in filtered:
        city = normalize_rc_name(rc)
        user = get_user_by_city(city)
        if user is None:
            none_cities.append(rc)
            continue

        data = text.split(" — ")

        shipment = create_shipment({
            "user_id": user.id,
            "user": user,
            "admin_id": admin_id,
            "city": city,
            "date": data[1] if len(data) > 1 else "",
            "status": "pending",
            "amount": data[2] if len(data) > 2 else 0,
        })

        await bot.send_message(
            chat_id=user.id,
            text=f"Доступен новый вывоз:\n{text}",
            reply_markup=partners_agreement_keyboard(shipment_id=shipment.id)
        )

        success_cities.append(rc)

    return none_cities, success_cities

