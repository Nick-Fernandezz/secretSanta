from telebot import types
from config import bot

from keyboard import main

from db import get_db
from db.main_db import cursor
from scripts import forms, head_group
from scripts.categories import all_students, local_group


def send_chat_id(message):
    bot.send_message(message.chat.id, message.chat.id)


def send_dev_message_send(message):

    cursor.execute('''SELECT user_id FROM users''')
    users = cursor.fetchall()

    for user in users:

        bot.send_message(user, f'Сообщение от администратора!\n\n{message.text}')


def send_dev_message_start(message):

    if message.from_user.id != '758055066':

        bot.send_message(message.from_user.id, 'У вас нет прав на это :(')
    else:
        send = bot.send_message(message.from_user.id, 'Введите текст для отправки.')

        bot.register_next_step_handler(send, send_dev_message_send)


def send_start_message(message):
    if message.chat.type != 'private':

        bot.send_message(message.chat.id, 'Для взаимодействия с ботом нажмите на кнопку ниже:',
                         reply_markup=main.keyboard_goto_bot)
    else:

        if message.from_user.username is None:
            bot.send_message(message.chat.id, 'У вас не настроен username. Тайный санта не сможет связаться с вами(\n'
                                              'Настройте username и напишите /start',
                             reply_markup=main.username_keyboard)
        else:
            bot.send_message(message.chat.id,
                             'Привет!\n'
                             'Это тайный санта!')
            get_db.create_new_user(message)

            start_keyboard = types.InlineKeyboardMarkup()
            start_keyboard.row(main.start_kb).row(main.head_kb)

            cursor.execute(f'''SELECT description FROM forms WHERE user_id = {message.from_user.id}''')
            desc = cursor.fetchone()

            if desc is not None:
                start_keyboard.row(main.my_form_kb)

            bot.send_message(message.chat.id,
                             'Тайный санта - отличный способ сделать приятно не только себе, но и совcесем незнакомому '
                             'человеку!\n'
                             'Продолжи и насладись этим приятным чувством, когда не только тебе дарят подарки, но и ты.',
                             reply_markup=start_keyboard)


def send_second_message(callback):
    bot.send_message(callback.message.chat.id,
                     'Санта очень рад, что ты решил участвовать в игре!\n'
                     'Для начала выбери в какой из категорий тебе интересно участвовать',
                     reply_markup=main.choose_category_keyboard)


def send_start_form(callback):
    forms.create_new_form(callback.message)


def register_start_message_handlers():
    bot.register_message_handler(send_chat_id, commands=['chat_id'])
    bot.register_message_handler(send_start_message, commands=['start'])
    bot.register_message_handler(send_dev_message_start, commands=['dev_mess'])
    bot.register_callback_query_handler(forms.send_form, func=lambda callback: callback.data == 'next_start')
    bot.register_callback_query_handler(forms.send_my_form, func=lambda callback: callback.data == 'my_form_cb')
    bot.register_callback_query_handler(local_group.add_to_local_group, func=lambda callback: callback.data == 'go_to_my_group')
    bot.register_callback_query_handler(all_students.add_to_all_students_category,
                                        func=lambda callback: callback.data == 'all_students')

    bot.register_callback_query_handler(head_group.new_head_group,
                                        func=lambda callback: callback.data == 'im_head_group')

