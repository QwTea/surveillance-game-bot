from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
class MainButtons:
    back_button = [
        [KeyboardButton(text="◀️ Вернуться")]]
    back_user_markup = ReplyKeyboardMarkup(keyboard=back_button, resize_keyboard=True)

    def all_chats(self, chats_title_and_id):
        main_keyboard = InlineKeyboardBuilder()
        
        if len(chats_title_and_id) < 0:
            main_keyboard.add(InlineKeyboardButton(text="Нет чатов", callback_data="no_chats"))
        else:
            for i in chats_title_and_id:
                main_keyboard.button(text=i[1], callback_data=f"chat_{i[0]}")
        main_keyboard.adjust(1)
        return main_keyboard.as_markup()