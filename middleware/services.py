from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.infrastructure.database import DatabaseConnector
from core.infrastructure.repositories import UserRepository
from core.infrastructure.services import (
    UserService,
)


class ServiceMiddleware(BaseMiddleware):
    def __init__(
        self, connector: DatabaseConnector,
    ):
        self.db_connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        
        # Repository
        user_repo = UserRepository(self.db_connector)
        
        # Service
        user_service = UserService(user_repo)
        
        services = {
            "user_service": user_service,
        }

        data.update(services)
        result = await handler(event, data)
        return result