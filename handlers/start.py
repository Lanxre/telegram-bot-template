from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from core.infrastructure.database.models import User
from core.infrastructure.services.user import UserService

base_router = Router()

@base_router.message(CommandStart())
async def command_start(message: Message, user_service: UserService) -> None:
    try:

        if message.from_user is None:
            await message.answer(
                text="Ошибка при запуске бота. Попробуйте позже.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return

        user = User.from_telegram(message.from_user)
        await user_service.create_user(user)
        await message.answer(text="Привет! Я бот.", reply_markup=ReplyKeyboardRemove())
    except Exception:
        await message.answer(
            text="Ошибка при запуске бота. Попробуйте позже.",
            reply_markup=ReplyKeyboardRemove(),
        )
