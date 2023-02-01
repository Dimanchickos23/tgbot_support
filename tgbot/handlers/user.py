import asyncio


from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command, state, Text
from aiogram.types import Message, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import text, bold, italic, code, pre

from tgbot.keyboards.main import keyboard


async def user_start(message: Message):

    await message.answer_sticker(sticker="CAACAgIAAxkBAAEBIDBioPXUu5rKDuhnPS3T_K7v5AJaGwAC3Q4AAk1d8Eso_al4IJZSniQE")
    await message.answer("Привет, " + message.from_user.first_name +
                         "! Это бот техподдержки доставки рационов питания" + text(bold(' Mealkit')), parse_mode=ParseMode.MARKDOWN)
    await asyncio.sleep(1)
    await message.answer("Меня зовут Кит. Чем могу помочь?", reply_markup=keyboard)
#async def user_start(message: Message):
   # await message.reply("Hello, user!")

async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/feedback', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(process_help_command, commands=["help"], state="*")
