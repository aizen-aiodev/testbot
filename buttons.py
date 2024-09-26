from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

email_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Obuna bolish', url='https://t.me/fg3g3g3gx/2')],
        [InlineKeyboardButton(text='Obunani tekshirish ☑️', callback_data='ch')]
    ]
)

hy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ha ✅', callback_data='true')],
        [InlineKeyboardButton(text='Yoq ❌', callback_data='false')]
    ]
)