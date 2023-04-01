
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from buttons.admin_buttons import MainButtons
from aiogram import types
from filters.filter_admin import IsAdmin
from modules.database import ChatDatabase
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile
import config

work_with_database = ChatDatabase()
router = Router()
admin_keyboards = MainButtons()

@router.message(Command("admin"), IsAdmin(admins_id=config.admins))
async def start_admin(message: types.Message):
    await message.answer("Привет админ\n\nВот список чатов в которых я нахожусь, выбери и я отправлю тебе файл с логами:", reply_markup=admin_keyboards.all_chats(work_with_database.get_chats()))

@router.callback_query(Text(startswith='chat_'))
async def send_txt_file(call: CallbackQuery):
    chat_id_for_file = call.data.split("_")[1]
    file_name = "data_txt_files/"+work_with_database.get_file_name(int(chat_id_for_file))
    fsi_file = FSInputFile(file_name)
    await call.message.answer_document(document=fsi_file)
    await call.answer("")
