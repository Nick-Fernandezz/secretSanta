from config import bot
from db.main_db import db, cursor
from keyboard import category

from telebot import types


def add_to_all_students_category(callback):

    cursor.execute(f'''UPDATE forms SET all_groups = True WHERE user_id = {callback.from_user.id}''')
    db.commit()

    global_game = types.InlineKeyboardMarkup()
    global_game.add(category.exit_from_global_game)

    bot.send_message(callback.message.chat.id, 'Вы добавлены в реестр глобальной игры.',
                     reply_markup=global_game)


def exit_global_game(callback):

    cursor.execute(f"""UPDATE forms SET all_groups = False WHERE user_id = {callback.from_user.id}""")
    db.commit()

    global_game = types.InlineKeyboardMarkup()
    global_game.add(category.join_in_global_game)

    bot.send_message(callback.message.chat.id, 'Вы удалены из глобального реестра игроков.',
                     reply_markup=global_game)


bot.register_callback_query_handler(exit_global_game, func=lambda callback: callback.data == 'exit_global_game')
bot.register_callback_query_handler(add_to_all_students_category,
                                    func=lambda callback: callback.data == 'join_global_game')
