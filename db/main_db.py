import psycopg2
from colorama import Fore

from config import login_db

db = psycopg2.connect(database =login_db['db'],
                      user=login_db['login'],
                      password=login_db['password'],
                      host=login_db['host'],
                      port=login_db['port'])
cursor = db.cursor()


def create_db_table():
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id bigint,
            username VARCHAR(150),
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            start_time INTEGER
        )""")
        db.commit()

        print(Fore.GREEN + '[DB] DB users created successful', Fore.RESET + '')
    except:
        print(Fore.RED + '[DB] DB users created ERROR', Fore.RESET + '')

    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS forms(
            id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id bigint NOT NULL,
            username VARCHAR(100),
            sex VARCHAR(100),
            age INTEGER,
            name_user VARCHAR(100),
            group_user INT,
            description VARCHAR(400),
            photo VARCHAR(100),
            all_groups BOOL DEFAULT FALSE,
            local_groups BOOL DEFAULT FALSE,
            status_local_group BOOL DEFAULT FALSE
        )''')
        db.commit()

        print(Fore.GREEN + '[DB] DB forms created successful', Fore.RESET + '')
    except:
        print(Fore.RED + '[DB] DB forms created ERROR', Fore.RESET + '')

    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS students_group(
            id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY ,
            group_name VARCHAR(100),
            head bigint,
            status BOOL DEFAULT False)''')
        db.commit()

        print(Fore.GREEN + '[DB] DB students_group created successful', Fore.RESET + '')
    except:
        print(Fore.RED + '[DB] DB students_group created ERROR', Fore.RESET + '')

    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS heads_groups(
            id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id bigint,
            first_name VARCHAR(150),
            last_name VARCHAR(150),
            group_name INT,
            head_phone VARCHAR(100),
            username_head VARCHAR(200)
        )''')
        db.commit()
        print(Fore.GREEN + '[DB] DB heads_groups created successful', Fore.RESET + '')
    except:
        print(Fore.RED + '[DB] DB heads_groups created ERROR', Fore.RESET + '')