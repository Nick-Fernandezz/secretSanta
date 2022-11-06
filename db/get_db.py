from colorama import Fore

from .main_db import cursor, db


def create_new_user(message) -> None:

    cursor.execute(f'SELECT * FROM users WHERE user_id={message.from_user.id}')
    user_inf = cursor.fetchone()

    if user_inf is None:
        cursor.execute("""
                        INSERT INTO users(user_id, username, first_name, last_name, start_time)
                        VALUES (%s, %s, %s, %s, %s)""",
                       (message.from_user.id, message.from_user.username, message.from_user.first_name,
                        message.from_user.last_name, message.date))
        db.commit()
        print(Fore.YELLOW + f'[INFO] New user[{message.from_user.id}] registered!', Fore.RESET + '')
    else:
        cursor.execute(f"""UPDATE users SET username = '{message.from_user.username}' 
        WHERE user_id = {message.from_user.id}""")


def check_user_form(user_id: str | int) -> bool:

    cursor.execute(f"""SELECT * FROM forms WHERE user_id = {int(user_id)}""")

    form = cursor.fetchone()

    if form is None:
        return False
    else:
        return True


def get_user_form(user_id: int | str):

    user = cursor.execute(f"""SELECT user_id, username, sex, age, name_user, FROM forms WHERE user_id={user_id}""")
    form_user_info = user.fetchall()

    return form_user_info
