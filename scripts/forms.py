from config import bot
from keyboard import form, main
from db.main_db import cursor, db

from db import get_db

from telebot import types


def end_form(message):

    description = message.text

    if len(description) > 400:
        send = bot.send_message(message.chat.id, 'Твой текст более 400 символов. Сократи его и отправь заного.')
        bot.register_next_step_handler(send, end_form)
    else:
        cursor.execute(f'''UPDATE forms SET description = '{description}' WHERE user_id = {message.from_user.id}''')
        db.commit()

        bot.send_message(message.chat.id, 'Анкета создана. '
                                          'Теперь выбери где ты категорию, в которой ты будешь участвовать',
                         reply_markup=main.choose_category_keyboard)


def send_description(callback):
    group = callback.data.split('_')[2]

    cursor.execute(f'''UPDATE forms SET group_user = '{group}' WHERE user_id = {callback.from_user.id}''')
    db.commit()

    send = bot.send_message(callback.message.chat.id,
                     'Осталось только написать описание.\n'
                     'Раскажи здесь о себе, своих интересах, услечениях, пожеланиях.\n'
                     'Постарайся уместить все в 400 символов.')
    bot.register_next_step_handler(send, end_form)


def send_group(message):
    try:
        age = int(message.text)
        cursor.execute(f"""UPDATE forms SET age = {age} WHERE user_id = {message.from_user.id}""")
        db.commit()

        cursor.execute('''SELECT group_name, id FROM students_group WHERE status = True''')
        groups = cursor.fetchall()

        for group in groups:
            group_kb = types.InlineKeyboardButton(text=f'{group[0].upper()}', callback_data=f'my_group_{group[1]}')
            form.groups_keyboard.add(group_kb)

        bot.send_message(message.chat.id, 'Выбери свою группу.\n'
                                          'Если твоей группы нет в списке, значит староста не внес ее в реестр.'
                                          'Обратись к старосте.', reply_markup=form.groups_keyboard)

    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка в параметрах, проверьте еще раз и попробуйте снова или '
                                          'напишите в ЛС администратору: https://t.me/nickishhh')


def send_age(callback):

    if callback.data == 'sex_male':
        cursor.execute(f"""UPDATE forms SET sex = %s WHERE user_id = {callback.from_user.id}""",
                       ('male',))
        db.commit()
    elif callback.data == 'sex_female':
        cursor.execute(f"""UPDATE forms SET sex = %s WHERE user_id = {callback.from_user.id}""",
                       ('female',))
        db.commit()

    send = bot.send_message(callback.message.chat.id, 'Введите свой возраст.\n'
                                                      '_Пример_: 5.', parse_mode='markdown')
    bot.register_next_step_handler(send, send_group)


def send_sex(message):
    cursor.execute("""INSERT INTO forms(user_id, username,name_user) VALUES (%s, %s, %s)""",
                   (message.from_user.id, message.from_user.username, message.text))
    db.commit()

    send = bot.send_message(message.chat.id, 'Выберите свой пол', reply_markup=form.sex_keyboard)

    bot.register_callback_query_handler(send, send_age)


def send_name(callback):

    cursor.execute(f'SELECT * FROM forms WHERE user_id={callback.from_user.id}')
    user_inf = cursor.fetchone()

    if user_inf is None:

        send = bot.send_message(callback.message.chat.id, 'Отправьте свое имя.\n'
                                               'Учитывайте, что по имени, которое вы указываете вам будут передавать '
                                               'подарок, поэтому указывайте полное *имя и фамилия*.',
                                parse_mode='markdown')

        bot.register_next_step_handler(send, send_sex)

    else:
        bot.send_message(callback.message.chat.id, 'Анкета уже создана')


def create_new_form(callback):

    bot.send_message(callback.message.chat.id, 'Отлично, можем приступить к созданию анкеты для игры!')
    bot.send_message(callback.message.chat.id, 'Нажимая кнопку "Продолжить", вы соглашаетесь с обработкой '
                                               'предоставляемы данных '
                                               'и передачей их другим участникам игры для коммуникации: '
                                               'Имя, пол, возраст',
                     reply_markup=form.go_to_next_keyboard)


def send_form(callback):
    form_user_info = get_db.check_user_form(callback.from_user.id)
    if form_user_info:

        form_keyboard = types.InlineKeyboardMarkup(row_width=1)
        form_keyboard.add(main.edit_form_kb, main.my_form_kb)

        bot.send_message(callback.message.chat.id, 'У тебя уже есть созданная анкета. '
                                                   'Ты можешь посмотреть ее или заполнить заного.',
                         reply_markup=form_keyboard)
    else:

        form_keyboard = types.InlineKeyboardMarkup(row_width=1)
        form_keyboard.add(main.create_form_kb)

        bot.send_message(callback.message.chat.id, 'Создай свою анкету!', reply_markup=form_keyboard)


def edit_form(callback):

    cursor.execute(f'''DELETE FROM forms WHERE user_id = {callback.from_user.id}''')
    db.commit()
    create_new_form(callback)



bot.register_callback_query_handler(send_name, func=lambda callback: callback.data == 'goto_next_form')
bot.register_callback_query_handler(send_description, func=lambda callback: 'my_group_' in callback.data)
bot.register_callback_query_handler(create_new_form, func=lambda callback: callback.data == 'create_form_cb')
bot.register_callback_query_handler(edit_form, func=lambda callback: callback.data == 'edit_form_cb')