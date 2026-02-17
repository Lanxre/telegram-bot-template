from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from core.infrastructure.database.models import User
from core.infrastructure.services.user import UserService

base_router = Router()

@base_router.message(CommandStart())
async def command_start(message: Message, user_service: UserService) -> None:
    try:
        user = User(
            id=message.from_user.id,
            is_bot=message.from_user.is_bot,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code,
            is_premium=bool(message.from_user.is_premium),
        )
        await user_service.create_user(user)
        await message.answer(text="Привет! Я бот.", reply_markup=ReplyKeyboardRemove())
    except Exception:
        await message.answer(
            text="Ошибка при запуске бота. Попробуйте позже.",
            reply_markup=ReplyKeyboardRemove(),
        )
