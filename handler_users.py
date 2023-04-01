
from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram import Bot
from modules.random_number import RandomNumber
from states.user_numbers_states import UserNumbers
from filters.filters_num import IsNumber
from filters.filters_chat_type import ChatTypeFilter
from modules.database import ChatDatabase
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated


work_with_database = ChatDatabase()
work_with_database.create_table()
router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))

@router.message(Command("start"))
async def start_bot(message: types.Message):
    await message.answer("Привет!\n\nДавай поиграем в игру угадай число\n\nЯ буду говорить больше или меньше число, а вы должны угадать его\n\nДля начала игры напиши команду /startGame")


@router.message(Command("startGame"))
async def start_bot(message: types.Message, state: FSMContext):
    await state.set_state(UserNumbers.random_numb)
    await state.update_data(random_number=RandomNumber.generate())
    await message.reply("Я загадал число, попробуй угадать его\n\nНапиши число от 1 до 1000")
    await state.set_state(UserNumbers.user_number)
    

@router.message(UserNumbers.user_number, IsNumber())
async def user_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    random_number = data.get("random_number")
    user_number = int(message.text)
    if user_number > random_number:
        await message.reply("Мое число меньше")
    elif user_number < random_number:
        await message.reply("Мое число больше")
    else:
        await message.reply("Ты угадал")
        await state.clear()

    

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    if work_with_database.get_file_name(event.chat.id) == None:
        work_with_database.add_chat(event.chat.id, event.chat.title)
        file_name = work_with_database.get_file_name(event.chat.id)
        text_about_chat = "Айди чата"+event.chat.id+" "+"название чата "+event.chat.title
        work_with_database.append_to_file(file_path=f"data_txt_files/{file_name}", text=text_about_chat)
        
        
        
        

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        if work_with_database.get_file_name(event.chat.id) == None:
            work_with_database.add_chat(event.chat.id, event.chat.title)
            file_name = work_with_database.get_file_name(event.chat.id)
            text_about_chat = "Айди чата"+str(event.chat.id)+" "+"название чата: "+event.chat.title+"\n"
            work_with_database.append_to_file(file_path=f"data_txt_files/{file_name}", text=text_about_chat)
    else:
        pass
    
@router.message(ChatTypeFilter(["group", "supergroup"]))
async def all_message(message):
    print(message)
    if message.caption != None:
        if message.reply_to_message == None:
            information_about_user = "user id:"+str(message.from_user.id)+" "+message.from_user.first_name+" написал/а: "+message.caption+" с отправкой фото или видео контента\n"
        else:
            try:
                information_about_user = "user id:"+str(message.from_user.id)+" "+message.from_user.first_name+"Ответил/а пользователю user id:"+str(message.reply_to_message.from_user.id)+" "+message.reply_to_message.from_user.first_name+" на сообщение "+message.reply_to_message.text+" вот так "+message.caption+" с отправкой фото или видео контента\n"
            except TypeError:
                information_about_user = "user id:"+str(message.from_user.id)+" "+message.from_user.first_name+"Ответил/а пользователю user id:"+str(message.reply_to_message.from_user.id)+" "+message.reply_to_message.from_user.first_name+" на сообщение "+message.reply_to_message.caption+" вот так "+message.caption+" с отправкой фото или видео контента (пользователь отправивший сообщение также отправил фото либо видео)\n"
        print(information_about_user)
        file_name = work_with_database.get_file_name(message.chat.id)
        work_with_database.append_to_file(file_path=f"data_txt_files/{file_name}", text=information_about_user)
    elif message.text == None:
        pass
    else:
        if message.reply_to_message == None:
            information_about_user = "user id:"+str(message.from_user.id)+" "+message.from_user.first_name+" написал/а: "+message.text+"\n"
        else:
            try:
                information_about_user = "user id:"+str(message.from_user.id)+" "+message.from_user.first_name+"Ответил/а пользователю user id:"+str(message.reply_to_message.from_user.id)+" "+message.reply_to_message.from_user.first_name+" на сообщение "+message.reply_to_message.text+" вот так "+message.text+"\n"
            except TypeError:
                information_about_user = "user id:"+str(message.from_user.id)+" "+message.from_user.first_name+"Ответил/а пользователю user id:"+str(message.reply_to_message.from_user.id)+" "+message.reply_to_message.from_user.first_name+" на сообщение "+message.reply_to_message.caption+" вот так "+message.text+" с отправкой фото или видео контента\n"
        print(information_about_user)
        file_name = work_with_database.get_file_name(message.chat.id)
        work_with_database.append_to_file(file_path=f"data_txt_files/{file_name}", text=information_about_user)