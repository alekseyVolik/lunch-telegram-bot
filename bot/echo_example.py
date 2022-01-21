from random import choice
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
from telegram import Update

from settings import BOT_TOKEN


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def simple_greeting(update: Update, context: CallbackContext) -> None:
    greet_pool = [
        'Привет', 'Приветсвую', 'Здрасте', 'Здравствуйте', 'Салам', 'Хой',
        'Бонжур епта', 'Hello', 'Hi', 'Guten Tag', '你好', 'Olá', 'こんにちは', None
    ]
    greeting_word = choice(greet_pool)

    if not greeting_word:
        current_time = datetime.now(tz=ZoneInfo("Europe/Samara"))
        current_hour = current_time.hour
        if 0 <= current_hour < 6:
            greeting_word = 'Доброй ночи'
        elif 6 <= current_hour < 12:
            greeting_word = 'Доброе утро'
        elif 12 <= current_hour < 18:
            greeting_word = 'Добрый день'
        else:
            greeting_word = 'Добрый вечер'

    sender = update.effective_user
    sender_name = sender.first_name if sender else 'Noname'
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{greeting_word}, {sender_name}!")


def unknown_command(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="На данный момент я не знаю такой команды :(")


def start(update: Update, context: CallbackContext) -> None:
    starting_message = "Я пока еще не такой умный (но ты все равно меня не сможешь уволить), " \
                       "поэтому мой список поддерживаемых команд невелик. " \
                       "Команды, которые мной поддерживаются:\n\n" \
                       "/greet - Обычное приветствие"
    context.bot.send_message(chat_id=update.effective_chat.id, text=starting_message)


greeting_handler = CommandHandler('greet', simple_greeting)
starting_handler = CommandHandler('start', start)
unknown_command_handler = MessageHandler(Filters.command, unknown_command)

dispatcher.add_handler(greeting_handler)
dispatcher.add_handler(starting_handler)
dispatcher.add_handler(unknown_command_handler)
updater.start_polling()
