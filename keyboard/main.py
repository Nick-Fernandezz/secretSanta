from telebot import types
from config import url_bot

username_keyboard = types.InlineKeyboardMarkup()
username_kb = types.InlineKeyboardButton(text='Как установить Username',
                                         url='https://web-telegramm.org/telegramm/web/608-kak-zapolnit-username-v-telegramme.html')
username_keyboard.add(username_kb)

keyboard_goto_bot = types.InlineKeyboardMarkup()
kb_goto_bot = types.InlineKeyboardButton(text='К Боту!', url=url_bot)
keyboard_goto_bot.add(kb_goto_bot)

start_form_keyboard = types.InlineKeyboardMarkup()
my_form_kb = types.InlineKeyboardButton(text='Моя анкета', callback_data='my_form_cb')
edit_form_kb = types.InlineKeyboardButton(text='Изменить анкету', callback_data='edit_form_cb')
create_form_kb = types.InlineKeyboardButton(text='Создать анкету', callback_data='create_form_cb')

start_keyboard = types.InlineKeyboardMarkup()
start_kb = types.InlineKeyboardButton(text='Продолжить', callback_data='next_start')
head_kb = types.InlineKeyboardButton(text='Я староста', callback_data='im_head_group')
start_keyboard.row(start_kb).row(head_kb).row(my_form_kb)


choose_category_keyboard = types.InlineKeyboardMarkup()
category_all = types.InlineKeyboardButton(text='Все студенты техникума', callback_data='all_students')
category_only_group = types.InlineKeyboardButton(text='Моя группа', callback_data='go_to_my_group')
choose_category_keyboard.add(category_all, category_only_group)
