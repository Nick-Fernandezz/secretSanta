from config import bot
from db.main_db import db, cursor
from keyboard import head_group
from scripts import admin


def new_head_group(callback):

    bot.send_message(callback.message.chat.id, 'Привет!\n'
                                               'Это консоль управления для старост своих групп.\n'
                                               'Доступ сюда разрешен только старостам.\n\n'
                                               'Выбери нужное действие, нажав на нужную кнопку.',
                     reply_markup=head_group.head_keyboard)


def add_grope_db(callback):
    send = bot.send_message(callback.message.chat.id, 'Введите полное название вашей группы.\n\n'
                                                      '_*Пример: _'
                                                      'ПР-1-9Б-22', parse_mode='markdown')

    bot.register_next_step_handler(send, check_grope_in_db)


def check_grope_in_db(message):

    group = message.text.lower()

    cursor.execute(f"""SELECT * FROM students_group WHERE group_name = '{group}'""")
    status_group = cursor.fetchone()

    if status_group is None:
        send = bot.send_message(message.chat.id, 'Группа не найдена в реестре.\n'
                                                 'Для начала давай зарегистрируемся, как староста.\n'
                                                 'Введи свое имя и фамилию.\n\n'
                                                 '_Пример_: Василий Пупкин',
                                parse_mode='markdown')

        cursor.execute(f'''INSERT INTO students_group(group_name, head) VALUES ('{group}', {message.from_user.id})''')
        db.commit()

        cursor.execute(f'''SELECT id FROM students_group WHERE head = {message.from_user.id}''')
        group_id = cursor.fetchone()[0]

        bot.register_next_step_handler(send, add_head_name, group_id)

    else:
        bot.send_message(message.chat.id, 'Ваша группа уже есть в реестре.\n'
                                          'Вы можете проверить статус своей группы.',
                         reply_markup=head_group.status_group_keyboard)


def add_head_name(message, group):

    head_name = message.text.split()
    try:
        cursor.execute(f'''SELECT * FROM heads_groups WHERE user_id = {message.from_user.id}''')
        user = cursor.fetchone()
        if user:
            cursor.execute(f"""UPDATE heads_groups SET first_name = %s, last_name = %s, group_name = %s
            WHERE user_id = {message.from_user.id}""",
                           (head_name[0], head_name[1], group))
            db.commit()
        else:
            cursor.execute("""INSERT INTO heads_groups(user_id, first_name, last_name, group_name, username_head) 
                        VALUES (%s, %s, %s, %s, %s)""",
                           (message.from_user.id, head_name[0], head_name[1], group, message.from_user.username))
            db.commit()

        send = bot.send_message(message.chat.id, 'Отлично!\n'
                                                 'Теперь отправь свой номер телефона.\n\n'
                                                 '_Пример:_ 71234567890',
                                parse_mode='markdown')
        bot.register_next_step_handler(send, add_phone_head)

    except:
        bot.send_message(message.chat.id, 'Ошибка в параметрах, проверьте еще раз и попробуйте снова или '
                                          'напишите в ЛС администратору: https://t.me/nickishhh')


def add_phone_head(message):

    phone = message.text

    if phone[:1] != '7':
        bot.send_message(message.chat.id, 'Номер должен начинаться на 7. Перепроверь номер и попробуй снова.')
    else:
        cursor.execute(f'''UPDATE heads_groups SET head_phone = '{phone}' WHERE user_id = {message.from_user.id}''')
        db.commit()

        bot.send_message(message.chat.id, 'Отлично!\n'
                                          'Вы зарегистрированы, как староста.\n'
                                          'Приступаю к регистрации группы....')

        cursor.execute(f"""SELECT user_id, group_name FROM heads_groups WHERE user_id = {message.from_user.id}""")
        user_info = cursor.fetchone()
        db.commit()

        bot.send_message(message.chat.id, 'Группа почти внесена в реестр.\n'
                                          'Ожидайте одобрения, после одобрения администратором, вам придет сообщение, '
                                          'а группу можно будет выбрать при создании анкеты.\n'
                                          'Будьте готовы к возможному звонку от администратора по указанному номеру.')

        admin.send_accept_group(message, user_info[0])


def send_status_head_group(callback):

    bot.send_message(callback.message.chat.id, 'Функция пока в разработке.')


bot.register_callback_query_handler(send_status_head_group, func=lambda callback: callback.data == 'group_status')
bot.register_callback_query_handler(add_grope_db, func=lambda callback: callback.data == 'add_grope_to_db')
