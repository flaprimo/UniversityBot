import logging
from telegram.ext import CommandHandler
from universitybot.translation import translate


class Help:
    """
    Greet a new user to the bot.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler("help", help))

        logger.info("Added /help command to Telegram handler")


'''
COMMAND VARIABLES
'''
# Utility
logger = logging.getLogger(__name__)


'''
COMMANDS
'''


def help(bot, update):
    user = update.message.from_user

    logger.info("%s[%s] started help command: %s" % (user.first_name, user['language_code'], update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Here\'s a list of the available commands:\n') +
                              '/provider - ' + _('Search for available classrooms\n') +
                              '/help - ' + _('Show how I can help you\n') +
                              '/info - ' + _('Get to know my parents\n'))
