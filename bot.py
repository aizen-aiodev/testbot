from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

import logging
import asyncio
import yagmail
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import token, admin
from filters import Channel
from state import Email
from buttons import email_kb, hy



email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# Вход в аккаунт Gmail

# yag = yagmail.SMTP('aizensbp086@gmail.com', 'supershox0909')

def is_valid_email(email):
    return re.match(email_regex, email) is not None

logging.basicConfig(level=logging.INFO)
bot = Bot(token)
dp = Dispatcher()



@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    if not Channel():
        await message.answer(text='Kanalga obuna boling 👤', reply_markup=email_kb)
    else:
        await message.answer(f'<b>👋 Salom {message.from_user.first_name}\nBu bot orqali siz Emailinguzga xabar yuboraolasiz 💬\n\nEmailni kiriting ✍️</b>', parse_mode=ParseMode.HTML)
        await state.set_state(Email.email)

@dp.callback_query(F.data == 'ch')
async def ch(call: types.CallbackQuery):
        if not Channel():
            await call.answer('Kanalga obuna boldingiz')
        else:
            await call.answer(text='Kanalga obuna boling', show_alert=True)

@dp.message(F.text, Email.email)
async def email(message: types.Message, state: FSMContext):
    email = message.text
    if is_valid_email(email):
        await state.update_data(
            {
                'email': email
            }
        )
        await state.set_state(Email.subject)
        await message.answer(f'{email} ga email tuboramiz\n\n Endi qaysi mavzuga yuboray') 
    else:
        await message.answer('Faqat Email')
        await state.clear()

@dp.message(F.text, Email.subject)
async def sub(message: types.Message, state: FSMContext):
    subject = message.text
    await state.update_data(
        {
            'subject':subject
        }
    )
    await state.set_state(Email.body)
    await message.answer('Endi xabar yuboring faqat text')

@dp.message(F.text, Email.body)
async def body(message: types.Message, state: FSMContext):
    body = message.text
    await state.update_data(
        {
            'body':body
        }
    )
    await state.set_state(Email.conf)
    await message.answer('Malumotlar saqlandi elarni yuboraymi? 📝', reply_markup=hy)

@dp.callback_query(F.data, Email.conf)
async def conf(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == 'true':
        msg = await state.get_data()
        email = msg.get('email')
        subject = msg.get('subject')
        body = msg.get('body')
        sender_email = "email_senderp16@mail.ru"
        receiver_email = email
        password = "86hVQGvMUesJ2GdEi00p"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        body = body
        msg.attach(MIMEText(body, 'plain'))
        # yag.send(to=email, subject=subject, contents=body)
        await call.message.answer(f'Email: {email} 📬\nMavzu: {subject} 📝\nXabar: {body} 💬\n\nYuborildi ✅')
        try:
            with smtplib.SMTP('smtp.mail.ru', 587) as server:  # Замените на ваш SMTP-сервер
                server.starttls()  # Защита соединения
                server.login(sender_email, password)  # Логин
                server.send_message(msg)  # Отправка сообщения
            print("Сообщение успешно отправлено")
        except Exception as e:
            print(f"Ошибка: {e}")

    else:
        await state.clear()
        await call.answer(text='Yuborilmadi ❌', show_alert=True)

async def main():
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print('Bot stopped')