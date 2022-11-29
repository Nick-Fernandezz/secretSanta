from config import bot
from db.main_db import cursor, db
from telebot import types


def add_to_local_group(callback):

    cursor.execute(f'''SELECT group_user, local_groups FROM forms WHERE user_id = {callback.from_user.id}''')
    user_group_info = cursor.fetchone()

    if user_group_info[1]:

        cursor.execute(f'''UPDATE forms SET local_group = True WHERE user_id = {callback.from_user.id}''')
        db.commit()
        bot.send_message(callback.message.chat.id, 'Вы внесены в реестр игроков своей группы.')
    else:

        bot.send_message(callback.message.chat.id, 'Отправляю заявку...')

        cursor.execute(f'''SELECT forms.user_id, forms.username, forms.sex, 
            forms.age, forms.name_user, forms.group_user, 
            forms.local_groups, heads_groups.user_id, heads_groups.username_head 
        FROM forms
        INNER JOIN heads_groups ON forms.group_user = heads_groups.group_name 
        WHERE forms.user_id = {callback.from_user.id}''')
        # cursor.execute(f'''SELECT user_id, username, sex, age, name_user, group_user, local_groups
        # FROM forms
        # WHERE user_id = {callback.from_user.id}''')
        # print(type(callback.from_user.id))
        # info_user = cursor.fetchone()
        # cursor.execute(f'''SELECT user_id, username_head FROM heads_groups WHERE group_name = {info_user[5]}''')
        # info_head = cursor.fetchone()
        # print(info_user[5])
        # print(info_head)
        info = cursor.fetchone()
        info_list = {
            'form_user_id': info[0],
            'username': info[1],
            'sex': info[2],
            'age': info[3],
            'name_user': info[4],
            'group_user': info[5],
            'local_group_starus': info[6],
            'head_user_id': info[7],
            'head_username': info[8]
        }

        if info_list['local_group_starus'] == 'True':
            info_list['local_group_starus'] = 'Одобрено'
        else:
            info_list['local_group_starus'] = 'Не одобрено'

        console_keyboard = types.InlineKeyboardMarkup()
        accept_kb = types.InlineKeyboardButton(text='✔', callback_data=f'accept_local_group_{info_list["form_user_id"]}')
        cross_kb = types.InlineKeyboardButton(text='❌', callback_data=f'cross_local_group_{info_list["form_user_id"]}')
        console_keyboard.add(accept_kb, cross_kb)

        bot.send_message(info_list['head_user_id'],
                         f"""@{info_list['head_username']}
Пришел новый запрос!
 
 От:
    Username: @{info_list['username']}
    Name: {info_list['name_user']} [{info_list['form_user_id']}]
    Sex: {info_list['sex']}
    
Status: {info_list['local_group_starus']}""",
                         reply_markup=console_keyboard)

        bot.send_message(callback.message.chat.id, 'Ваша заявка отправлена на рассмотрение старостой группы.\n'
                                                   'После проверки вам придет сообщение о статусе заявки.')


def accept_to_local_group(callback):

    user_id = callback.data.split('_')[3]

    cursor.execute(f'''UPDATE forms SET status_local_group = True WHERE user_id = {user_id}''')
    db.commit()

    cursor.execute(f'''UPDATE forms SET local_groups = True WHERE user_id = {user_id}''')
    db.commit()

    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text=callback.message.text + '\n\n ОДОБРЕНО!')
    bot.send_message(user_id, 'Ваша заявка одобрена и вы включены в реестр игры вашей группы.\n'
                              'Дальнейшие вопросы можете решать с администратором: https://t.me/nickishhh')


def cross_to_local_group(callback):
    user_id = callback.data.split('_')[3]

    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text=callback.message.text + '\n\n ОТКАЗАНО!')

    bot.send_message(user_id, 'В вашей заявке отказано...\n'
                              'Дальнейшие вопросы можете решать со старостой')


bot.register_callback_query_handler(accept_to_local_group, func=lambda callback: 'accept_local_group_' in callback.data)
bot.register_callback_query_handler(cross_to_local_group, func=lambda callback: 'cross_local_group_' in callback.data)

