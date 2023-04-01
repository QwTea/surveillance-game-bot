from aiogram import types
from aiogram.filters import BaseFilter


class IsNumber(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        
        # Проверяем, что текст сообщения состоит только из цифр
        if message.text.isdigit():
            return True
        else:
            return False