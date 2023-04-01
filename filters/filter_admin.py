from aiogram import types
from aiogram.filters import BaseFilter
from typing import Union



class IsAdmin(BaseFilter):
    def __init__(self, admins_id: Union[int, list]) -> None:
        self.admins_id = admins_id
                
    async def __call__(self, message: types.Message) -> bool:
        
        if message.chat.id in self.admins_id:
            return True
        else:
            return False
