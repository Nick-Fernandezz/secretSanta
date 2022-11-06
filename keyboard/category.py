from telebot import types


join_in_global_game = types.InlineKeyboardButton(text='Играть со всеми', callback_data='join_global_game')
exit_from_global_game = types.InlineKeyboardButton(text='Выйти из глобальной игры', callback_data='exit_global_game')

