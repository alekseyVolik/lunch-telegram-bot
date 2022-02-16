from bot.bot_enum.chat_commands import ChatCommands


class ChatCommandRegister:

    def __init__(self):
        self.commands = {}

    def register_command(self, chat_command: ChatCommands):
        self.commands[chat_command.command] = chat_command.description

        def action_wrapper(action):
            return action

        return action_wrapper

    def as_string(self):
        return '\n'.join(
            (f"/{chat_command}: {description}" for chat_command, description in self.commands.items())
        )
