from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram import Update

from bot.storage.manipulation.user_manipulation import add_user
from bot.storage.manipulation.user_manipulation import get_signed_user
from bot.storage.manipulation.user_manipulation import update_check_in_status
from bot.storage.manipulation.user_manipulation import get_user_by_id
from bot.storage.manipulation.user_manipulation import update_status

from bot.singleton import user_storage
from bot.singleton import chat_command_register

from bot.bot_enum.chat_commands import ChatCommands

from settings import BOT_TOKEN


@chat_command_register.register_command(ChatCommands.start)
def start(update: Update, context: CallbackContext) -> None:
    starting_message = f"Привет! Этот бот создан для совместного похода покушать в приятной компании людей\n\n " \
                       f"Следующие комманды доступны:\n{chat_command_register.as_string()}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=starting_message)


@chat_command_register.register_command(ChatCommands.subscribe)
def user_sign(update: Update, context: CallbackContext) -> None:
    telegram_user = update.effective_user
    storage_user = get_user_by_id(storage=user_storage, user_id=telegram_user.id)
    if storage_user:
        if storage_user['status']:
            text = f'{telegram_user.first_name}, Вы уже подписаны!'
        else:
            text = f'С возвращением, {telegram_user.first_name}!'
            update_status(storage=user_storage, user_id=telegram_user.id, status=True)
    else:
        text = f'Добро пожаловать, {telegram_user.first_name}!'
        user = {
            '_id': telegram_user.id,
            'first_name': telegram_user.first_name,
            'last_name': telegram_user.last_name if telegram_user.last_name else '',
            'check_in': False,
            'status': True
        }
        add_user(storage=user_storage, user_info=user)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


@chat_command_register.register_command(ChatCommands.unsubscribe)
def user_unsign(update: Update, context: CallbackContext) -> None:
    telegram_user = update.effective_user
    storage_user = get_user_by_id(storage=user_storage, user_id=telegram_user.id)
    if storage_user:
        if storage_user['status']:
            text = f'{telegram_user.first_name}, как жаль что Вы отписываетесь от нас :"('
            update_status(storage=user_storage, user_id=telegram_user.id, status=False)
        else:
            text = f'{telegram_user.first_name}, Вы уже отписаны от нас :/'
    else:
        text = f'{telegram_user.first_name}, Вы даже еще не подписывались :('
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


@chat_command_register.register_command(ChatCommands.notify_me)
def user_check(update: Update, context: CallbackContext) -> None:
    telegram_user = update.effective_user
    storage_user = get_user_by_id(storage=user_storage, user_id=telegram_user.id)
    if storage_user and storage_user['status']:
        update_check_in_status(storage=user_storage, user_id=storage_user['_id'], status=True)
        text = f'{storage_user["first_name"]} сегодня в офисе!'
    else:
        text = f'{telegram_user.first_name}, сначало необходимо подписаться на бота: выполнить команду /sign'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


@chat_command_register.register_command(ChatCommands.member_list)
def member_list(update: Update, context: CallbackContext) -> None:
    _member_list = '\n'.join(
        [f'[{"+" if user["check_in"] else "-"}]  '
         f'{user["first_name"]} '
         f'{user["last_name"]}'
         for user in get_signed_user(storage=user_storage)]
    )
    text = f'Список пользователей:\n\n' \
           f'{_member_list if _member_list else "Никого нету :("}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


if __name__ == '__main__':
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    command_start = CommandHandler('start', start)
    command_user_sign = CommandHandler('sign', user_sign)
    command_user_insign = CommandHandler('unsign', user_unsign)
    command_member_list = CommandHandler('member_list', member_list)
    command_check_in = CommandHandler('check_in_me', user_check)

    dispatcher.add_handler(command_start)
    dispatcher.add_handler(command_user_sign)
    dispatcher.add_handler(command_user_insign)
    dispatcher.add_handler(command_member_list)
    dispatcher.add_handler(command_check_in)

    updater.start_polling()
