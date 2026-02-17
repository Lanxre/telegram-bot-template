from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

base_router = Router()

@base_router.message(CommandStart())
async def command_start(message: Message) -> None:
    try:
       await message.answer(text="Привет! Я бот.", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        await message.answer(
            text=f"Ошибка при запуске бота: {str(e)}",
            reply_markup=ReplyKeyboardRemove(),
        )
