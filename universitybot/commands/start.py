import logging
from telegram.ext import CommandHandler
from universitybot.translation import translate


class Start:
    """
    Greet a new user to the bot.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler("start", start))

        logger.info("Added /start command to Telegram handler")


'''
COMMAND VARIABLES
'''
# Utility
logger = logging.getLogger(__name__)


'''
COMMANDS
'''


def start(bot, update):
    user = update.message.from_user

    logger.info("%s[%s] started start command: %s" % (user.first_name, user['language_code'], update.message.text))
    translate(user['language_code'])

    update.message.reply_text(_('Hi ') + user.first_name + '!\n' +
                              _('I\'m here to help you survive at Politecnico di Milano (or at least I try),\n'
                                'to know what I can do for you just ask for some /help !'))
