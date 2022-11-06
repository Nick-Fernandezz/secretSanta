
from colorama import Fore
from art import tprint

from config import bot
from handlers import main

from db import main_db
from db import get_db

tprint('SECRET   SANTA   BOT')
print(Fore.CYAN + 'Created by Nick Fernandez', Fore.RESET + '\n\n')


main_db.create_db_table()  # Create db table


main.register_start_message_handlers()


if __name__ == '__main__':
    print(Fore.GREEN + '[BOT] Bot started!', Fore.RESET + '')
    bot.infinity_polling()
