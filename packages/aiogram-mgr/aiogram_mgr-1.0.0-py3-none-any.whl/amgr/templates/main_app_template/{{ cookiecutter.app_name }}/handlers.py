from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="Main")  # Feel free to change the router name.


@router.message(Command('start'))
async def start_handler(message: Message):
	await message.answer("Bot is working!")
