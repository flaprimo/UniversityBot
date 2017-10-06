import logging
import telegram
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove
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


@translate
def start(bot, update):
    user = update.message.from_user

    logger.info("%s[%s] started start command: %s" % (user.first_name, user['language_code'], update.message.text))

    update.message.reply_text(_('*Hi %(user)s!*\n\n'
                                'I\'m here to help you at Politecnico di Milano,\n'
                                'to know what I can do for you just ask for some /help!')
                              % {'user': user.first_name},
                              disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=telegram.ParseMode.MARKDOWN)
