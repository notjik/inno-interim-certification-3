from aiogram import Bot, types


async def set_starting_commands(bot: Bot, chat_id: int):
    commands = {
        'ru': [
            types.BotCommand('start', 'Начать работу с ботом'),
            types.BotCommand('about', 'Информация о себе'),
        ],
        'en': [
            types.BotCommand('start', 'Start working with a bot'),
            types.BotCommand('about', 'Information about yourself'),
        ]
    }
    for lang, comm in commands.items():
        await bot.set_my_commands(
            commands=comm,
            scope=types.BotCommandScopeChat(chat_id),
            language_code=lang
        )