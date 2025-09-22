import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.controllers.users import check_role

class AccessMiddleware(BaseMiddleware):
    def __init__(self, role: str):
        self.role = role
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if check_role(user_id, self.role):
            return await handler(event, data)
        else:
            return None