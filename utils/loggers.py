import sys
import logging

if __name__ == '__main__':
    exit('Use it as a module.')
else:
    logger_message = logging.getLogger('messages')
    logger_message.setLevel(logging.INFO)
    formatter_messages = logging.Formatter("[%(asctime)s]: <%(levelname)s> "
                                           "%(user)s[%(user_id)d] send %(content_type)s\ndetailed: %(message)s\n",
                                           datefmt="%Y-%m-%d %H:%M:%S")
    _handler_logfile = logging.FileHandler(f"data/messages.log", mode='a')
    _handler_logfile.setFormatter(formatter_messages)
    _handler_console = logging.StreamHandler(sys.stdout)
    _handler_console.setFormatter(formatter_messages)
    logger_message.addHandler(_handler_logfile)
    logger_message.addHandler(_handler_console)

    logger_status = logging.getLogger('status')
    logger_status.setLevel(logging.INFO)
    formatter_messages = logging.Formatter("[%(asctime)s]: <%(levelname)s> "
                                           "The %(bot)s[%(bot_id)d] %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S")
    _handler_logfile = logging.FileHandler(f"data/status.log", mode='a')
    _handler_logfile.setFormatter(formatter_messages)
    _handler_console = logging.StreamHandler(sys.stdout)
    _handler_console.setFormatter(formatter_messages)
    logger_status.addHandler(_handler_logfile)
    logger_status.addHandler(_handler_console)

