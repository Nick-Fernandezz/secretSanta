import config
from config import bot, admin_chat
from db.main_db import db, cursor
from keyboard import admin
from telebot import types


def send_accept_group(message, head_id):

    cursor.execute(f"""SELECT students_group.id, students_group.group_name, 
    students_group.head, students_group.status, heads_groups.first_name, 
    heads_groups.last_name, heads_groups.head_phone, 
    heads_groups.username_head 
    FROM students_group 
    INNER JOIN heads_groups ON students_group.head = heads_groups.user_id 
    WHERE head = {head_id}""")
    info = cursor.fetchone()

    info_list = {
        'group_id': info[0],
        'group_name': info[1],
        'head_id': info[2],
        'groupe_status': info[3],
        'head_first_name': info[4],
        'head_last_name': info[5],
        'head_phone': info[6],
        'head_username': info[7]
    }

    if info_list['groupe_status']:
        info_list['groupe_status'] = 'Одобрено'
    else:
        info_list['groupe_status'] = 'Не одобрено'

    console_keyboard = types.InlineKeyboardMarkup()
    accept_kb = types.InlineKeyboardButton(text='✔', callback_data=f'accept_head_{head_id}')
    cross_kb = types.InlineKeyboardButton(text='❌', callback_data=f'cross_head_{head_id}')
    console_keyboard.add(accept_kb, cross_kb)

    bot.send_message(config.admin_chat,
                     f"""Пришел новый запрос!
Отправитель:
    Username: @{info_list['head_username']} [{info_list['head_id']}]
    Name: {info_list['head_first_name']} {info_list['head_last_name']}
    Phone: +{info_list['head_phone']}

Группа:
    ID: {info_list['group_id']}
    Name: {info_list['group_name']}
    Status: {info_list['groupe_status']}""",
                     reply_markup=console_keyboard)


def accept_group(callback):

    head_id = callback.data.split('_')[2]

    cursor.execute(f'''UPDATE students_group SET status = True WHERE head = {head_id}''')
    db.commit()
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text=callback.message.text + '\n\n ОДОБРЕНО!')
    bot.send_message(head_id, 'Ваша группа одобрена и теперь видна при создании анкеты.\n'
                              'Дальнейшие вопросы можете решать с администратором: https://t.me/nickishhh')


def cross_group(callback):
    head_id = callback.data.split('_')[2]

    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text=callback.message.text + '\n\n ОТКАЗАНО!')

    bot.send_message(head_id, 'Вашей группе отказано в добавлении в реестр.\n'
                              'Дальнейшие вопросы можете решать с администратором: https://t.me/nickishhh')


bot.register_callback_query_handler(accept_group, func=lambda callback: 'accept_head_' in callback.data)
bot.register_callback_query_handler(cross_group, func=lambda callback: 'cross_head_' in callback.data)
