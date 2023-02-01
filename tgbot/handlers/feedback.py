import emoji
import pandas as pd
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers.user import keyboard
from tgbot.misc.states import Test

df = pd.read_excel("/Users/Dmitry Klimenko/Desktop/Mealkit_Bot/tgbot/handlers/data.xlsx")

yes_no = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=
                                  [
                                      [
                                          InlineKeyboardButton(
                                              text="Да 👍",
                                              callback_data='Да'
                                          ),
                                          InlineKeyboardButton(
                                              text="Нет 👎",
                                              callback_data='Нет'
                                          )
                                      ]
                                  ]
                                  )

#@Dispatcher.message_handler(Command("feedback"))
async def feedback_start(message: Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEBI3Nip3dGSI77i1SuPBMqlDJ-UytzYQACJhAAAnep8Es_tBwk-BeUKiQE",
                                 reply_markup=types.ReplyKeyboardRemove())
    await Test.Q1.set()
    await message.answer(message.from_user.full_name
                         + ", вам понравился ваш рацион?",reply_markup=yes_no )
    await state.update_data(name=message.from_user.first_name,
                            surname=message.from_user.last_name,
                            id=message.from_user.id,
                            date=message.date)
    #await Test.first()


async def Q1_answer(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(q1=answer)
    if (answer == 'Да'):
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEBI3dip3vdIHdPHGznEqnKZc_Wrc9j3wACFw4AAu9lUEhF0ygYG6bV5iQE")
        await callback.message.answer("Есть пожелания и предложения?")
    else:
        await callback.message.answer_sticker(
            sticker="CAACAgIAAxkBAAEBI3tip3z1jkwAAQjQ3fl3b82J34GpvpsAApcNAAJvivBLcCAac8Fe0HQkBA")
        await callback.message.answer("Почему? Опишите причину, по которой вам не понравились наши рационы.")


    await Test.next()

async def Q2_answer(message: Message, state: FSMContext):
    await state.update_data(q2=message.text)
    data = await state.get_data()
    #await message.answer(f"Ваше имя: "+ data.get("name"))
    #await message.answer(f"Ваша фамилия: "+ data.get("surname"))
    #await message.answer(f"Ваш Telegram id: "+ str(data.get("id")))
    #await message.answer(f"Ответ 1: " + str(data.get("q1")))
    #await message.answer(f"Ответ 2: " + str(data.get("q2")))
    df.loc[len(df.index)] = data
    df.to_excel("/Users/Dmitry Klimenko/Desktop/Mealkit_Bot/tgbot/handlers/data.xlsx",index=False)
    await state.finish()
    await message.answer("Спасибо!  Мы обязательно все учтем и станем лучше.",reply_markup=keyboard)
    #await state.reset_state(with_data=False)
    #сбросить состояние не стирая собранные данные

async def if_not_query(message: Message, state: FSMContext):
    await message.answer_sticker("CAACAgIAAxkBAAEBI39ip4EB7unOgbngNgdicjl8BTtCvAACHwwAAr9_OUl5W2p_J1WxryQE")
    await message.answer("Я не понимаю, выберите вариант ответа ниже."+ emoji.emojize(":down_arrow:"),reply_markup=yes_no)

async def if_not_text(message: Message, state: FSMContext):
    await message.answer_sticker("CAACAgIAAxkBAAEBI39ip4EB7unOgbngNgdicjl8BTtCvAACHwwAAr9_OUl5W2p_J1WxryQE")
    await message.answer("Я не понимаю. Введите, пожалуйста, ваш ответ с клавиатуры."+ emoji.emojize(":down_arrow:"))

def register_feedback(dp: Dispatcher):
    dp.register_message_handler(feedback_start, lambda message: message.text == "📝 Оставить отзыв", state="*")
    dp.register_callback_query_handler(Q1_answer,lambda callback_query: True, state=Test.Q1)
    dp.register_message_handler(if_not_query, state=Test.Q1, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(Q2_answer, state=Test.Q2)
    dp.register_message_handler(if_not_text, state=Test.Q2, content_types=types.ContentTypes.ANY)