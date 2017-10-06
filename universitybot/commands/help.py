import logging
from telegram.ext import CommandHandler
from universitybot.translation import translate


class Help:
    """
    Help the user by listing the bot functionalities.
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


@translate
def help(bot, update):
    user = update.message.from_user

    logger.info("%s[%s] started help command: %s" % (user.first_name, user['language_code'], update.message.text))

    command_list = [
        ('/freeclassrooms', _('search for free classrooms')),
        ('/links', _('useful links')),
        ('/help', _('list available commands')),
        ('/credits', _('bot creators'))]

    command_string = ''
    for command in command_list:
        command_string += '\n{} - {}'.format(command[0], command[1])

    update.message.reply_text(_('How can I help you?') + '\n' + command_string)
