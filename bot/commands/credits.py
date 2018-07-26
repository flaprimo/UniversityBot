import gettext
import logging

import telegram
from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)


class Credits:
    """
    Greet a new user to the bot.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler('credits', self.credits))

        logger.info('Added /credits command to Telegram handler')

    @staticmethod
    def credits(bot, update):
        user = update.message.from_user

        logger.debug('%s[%s] started info command: %s' % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('I was created by:\n\n[Flavio Primo](https://t.me/flaprimo) - you can follow him '
                                    'at [https://flavioprimo.xyz/](https://flavioprimo.xyz/)\n[Paolo Paterna]('
                                    'https://t.me/TopoDiFogna) - you can follow him at [https://paterna.tk/]('
                                    'https://paterna.tk/)')

        bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN,
                         disable_web_page_preview=True)
