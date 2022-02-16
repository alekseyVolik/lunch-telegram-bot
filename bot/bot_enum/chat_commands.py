from enum import Enum


class ChatCommands(Enum):

    start = (
        'start',
        'Начальная команда'
    )

    subscribe = (
        'subscribe',
        'позволяет подписаться на бота и получать уведомления о сборе, '
        'принимать голосование в изменение места и времени ланча'
    )

    unsubscribe = (
        'unsubscribe',
        'отписаться от бота, функциональность бота становится недоступной'
    )

    notify_me = (
        'notify_me',
        'позволяет отметиться как присутствующему в офисе человеку'
    )

    member_list = (
        'member_list',
        'список подписавшихся сотрудников со статусом отметки присутсвия '
        'в офисе, формат: (+ или -) Имя [Фамилия]'
    )

    def __init__(self, command: str, description: str):
        self.command = command
        self.description = description
