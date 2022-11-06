
from config import bot

from keyboard import main

from db import get_db
from scripts import forms, head_group
from scripts.categories import all_students, local_group


def send_chat_id(message):
    bot.send_message(message.chat.id, message.chat.id)


def send_start_message(message):
    if message.chat.type != 'private':

        bot.send_message(message.chat.id, 'Для взаимодействия с ботом нажмите на кнопку ниже:',
                         reply_markup=main.keyboard_goto_bot)
    else:

        if message.from_user.username == 'None':
            bot.send_message(message.chat.id, 'У вас не настроен username. Тайный санта не сможет связаться с вами(\n'
                                              'Настройте username и напишите /start',
                             reply_markup=main.username_keyboard)
        else:
            bot.send_message(message.chat.id,
                             'Привет!\n'
                             'Это тайный санта!')
            get_db.create_new_user(message)

            bot.send_message(message.chat.id,
                             'Тайный санта - отличный способ сделать приятно не только себе, но и совcесем незнакомому '
                             'человеку!\n'
                             'Продолжи и насладись этим приятным чувством, когда не только тебе дарят подарки, но и ты.',
                             reply_markup=main.start_keyboard)


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
    bot.register_callback_query_handler(forms.send_form, func=lambda callback: callback.data == 'next_start')
    bot.register_callback_query_handler(forms.send_my_form, func=lambda callback: callback.data == 'my_form_cb')
    bot.register_callback_query_handler(local_group.add_to_local_group, func=lambda callback: callback.data == 'go_to_my_group')
    bot.register_callback_query_handler(all_students.add_to_all_students_category,
                                        func=lambda callback: callback.data == 'all_students')

    bot.register_callback_query_handler(head_group.new_head_group,
                                        func=lambda callback: callback.data == 'im_head_group')

