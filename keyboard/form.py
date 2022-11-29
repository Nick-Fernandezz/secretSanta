from telebot import types

go_to_next_keyboard = types.InlineKeyboardMarkup()
next_kb = types.InlineKeyboardButton(text='Продолжить', callback_data='goto_next_form')
go_to_next_keyboard.add(next_kb)

sex_keyboard = types.InlineKeyboardMarkup()
male_kb = types.InlineKeyboardButton(text='Я парень', callback_data='sex_male')
female_kb = types.InlineKeyboardButton(text='Я девушка', callback_data='sex_female')
sex_keyboard.add(male_kb, female_kb)



