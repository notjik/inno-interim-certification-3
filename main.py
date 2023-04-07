"""
Реализовать бота, приветствующего пользователя при вводе команды /start и выводящего информацию о себе при вводе команды /about.
"""
# *You need to download: "aiogram", "python-dotenv"*
# *You need to add a token, host, path to the environment variable*

# Imports for working with a bot
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor, exceptions
from dotenv import load_dotenv
from utils.loggers import logger_message, logger_status
from utils.menu import set_starting_commands

# Loading environment variables
load_dotenv()

# Unloading local variables and initializing the bot
try:
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
    WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH
    WEBAPP_HOST = os.getenv('WEBAPP_HOST')
    WEBAPP_PORT = os.getenv('WEBAPP_PORT')
    bot = Bot(token=os.getenv('TOKEN'))
except TypeError as e:
    exit('Create local variables: {}'.format(e))
dispatcher = Dispatcher(bot)


async def startup(callback):
    """
    Logging the launch of the bot

    :param callback: dispatcher object
    :return: None
    """
    await bot.set_webhook(WEBHOOK_URL)
    me = await callback.bot.get_me()
    extra = {
        'bot': me.username,
        'bot_id': me.id,
    }
    logger_status.info('has been successfully launched.', extra=extra)


async def shutdown(callback):
    """
    Logging off the bot

    :param callback: dispatcher object
    :return: None
    """
    await bot.delete_webhook()
    me = await callback.bot.get_me()
    extra = {
        'bot': me.username,
        'bot_id': me.id,
    }
    logger_status.info('is disabled.', extra=extra)


@dispatcher.message_handler(filters.CommandStart())
async def start_message(msg: types.Message):
    """
    The starting message of the bot

    :param msg: message object
    :return: answer
    """
    await msg.answer('Hi, @{}!'.format(msg.from_user.username))  # Request with a message to the user
    await set_starting_commands(bot, msg.chat.id)
    extra = {
        'user': msg.from_user.username,
        'user_id': msg.from_user.id,
        'content_type': '/start'
    }
    logger_message.info(msg, extra=extra)


@dispatcher.message_handler(filters.Command('about'))
async def about_message(msg: types.Message):
    """
    The help message of the bot

    :param msg: message object
    :return: answer
    """
    print(msg.from_user)
    await msg.answer("Name: {}\n"
                     "User: {}[{}]\n"
                     "Language: {}\n"
                     "Locale: {}\n"
                     "{}".format(msg.from_user.full_name,
                                 msg.from_user.username,
                                 msg.from_user.id,
                                 msg.from_user.language_code,
                                 msg.from_user.locale,
                                 "\nHas a premium" if msg.from_user.is_premium else ''))
    extra = {
        'user': msg.from_user.username,
        'user_id': msg.from_user.id,
        'content_type': '/help'
    }
    logger_message.info(msg, extra=extra)


@dispatcher.errors_handler(exception=exceptions.BotBlocked)
async def except_bot_blocked(update: types.Update, exception: exceptions.BotBlocked):
    extra = {
        'user': update.message.from_user.username,
        'user_id': update.message.from_user.id,
        'content_type': 'the bot to the ban'
    }
    logger_message.warning(update.message, extra=extra)
    return True


# Entry point
if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dispatcher,
        webhook_path=WEBHOOK_PATH,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        on_startup=startup,
        on_shutdown=shutdown,
        skip_updates=True,
    )  # Launching webhook
