import gettext
import logging

import telegram
from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)


class Help:
    """
    Help the user by listing the bot functionalities.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler('help', self.help))

        logger.info('Added /help command to Telegram handler')

    @staticmethod
    def help(bot, update):
        user = update.message.from_user

        logger.debug('%s[%s] started help command: %s' % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', 'bot/locale', languages=[user['language_code']], fallback=True)

        command_list = [
            ('/classroominfo', translation.gettext('get classroom info (building, photo, notes, directions)')),
            ('/freeclassrooms', translation.gettext('search for free classrooms')),
            ('/links', translation.gettext('useful links')),
            ('/help', translation.gettext('list available commands')),
            ('/credits', translation.gettext('bot creators'))]

        reply = ''
        for command in command_list:
            reply += '\n%s - %s' % (command[0], command[1])

        reply = translation.gettext('How can I help you?') + '\n' + reply

        bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
