import gettext
import logging

import telegram
from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)


class Start:
    """
    Greet a new user to the bot.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))

        logger.info("Added /start command to Telegram handler")

    @staticmethod
    def start(bot, update):
        user = update.message.from_user

        logger.debug("%s[%s] started start command: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = (translation.gettext('*Hi %s!*\n\nI\'m here to help you at Politecnico di Milano, to know what I can '
                                     'do for you just ask for some /help!') % user.first_name)

        bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
