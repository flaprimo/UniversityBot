import logging
import telegram
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove
from universitybot.translation import translate


class Credits:
    """
    Greet a new user to the bot.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler("credits", credits))

        logger.info("Added /info command to Telegram handler")


'''
COMMAND VARIABLES
'''
# Utility
logger = logging.getLogger(__name__)


'''
COMMANDS
'''


@translate
def credits(bot, update):
    user = update.message.from_user

    logger.info("%s[%s] started info command: %s" % (user.first_name, user['language_code'], update.message.text))

    update.message.reply_text(_('I was created by:') + '\n\n' +
                              '[Flavio Primo](https://t.me/flaprimo) - ' +
                              _('you can follow him at [https://flavioprimo.xyz/](https://flavioprimo.xyz/)') + '\n'
                              '[Paolo Paterna](https://t.me/TopoDiFogna) - ' +
                              _('you can follow him at [https://paterna.tk/](https://paterna.tk/)'),
                              disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=telegram.ParseMode.MARKDOWN)
