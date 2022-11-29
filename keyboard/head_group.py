from telebot import types

head_keyboard = types.InlineKeyboardMarkup(row_width=1)
status_group_keyboard = types.InlineKeyboardMarkup()

add_group_kb = types.InlineKeyboardButton(text='Добавить группу в реестр', callback_data='add_grope_to_db')
get_group_status = types.InlineKeyboardButton(text='Статус моей группы', callback_data='group_status')

head_keyboard.add(add_group_kb, get_group_status)
status_group_keyboard.add(get_group_status)

list_users_keyboard = types.InlineKeyboardMarkup()
list_users_kb = types.InlineKeyboardButton(text='Список участников', callback_data='list_users')
list_users_keyboard.add(list_users_kb)
