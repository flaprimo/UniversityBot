import logging
from telegram.ext import CommandHandler
from lib.Translation import translate


class Info:
    """
    Greet a new user to the bot.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler("info", info))

        logger.info("Added Info command to Telegram handler")


'''
COMMAND VARIABLES
'''
# Utility
logger = logging.getLogger(__name__)


'''
COMMANDS
'''


def info(bot, update):
    user = update.message.from_user

    logger.info("%s started info command: %s" % (user.first_name, update.message.text))

    translate(user['language_code'])

    update.message.reply_text(_('Here I proudly present my parents!\n') +
                              'Flavio Primo - ' + _('You can follow his ramblings here https://flavioprimo.xyz/'))
