from typing import Any
from aiogram.filters import Filter
from aiogram import Bot
from aiogram.types import Message

class Channel(Filter):
    async def __call__(self, message: Message, bot: Bot):
        user_status = await bot.get_chat_member(-1002271564891, message.from_user.id)
        if user_status.status in ['creator', 'administrator', 'member']:
            return False
        return True