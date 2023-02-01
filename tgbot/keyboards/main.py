from aiogram import Dispatcher, types

kb = [
        [
            types.KeyboardButton(text="🌍 Мы в Соцсетях"),
            types.KeyboardButton(text="📝 Оставить отзыв")
        ],
        [
            types.KeyboardButton(text="💸 Оплата"),
            types.KeyboardButton(text="🦸‍ Связь с оператором")
        ]
    ]

keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите")