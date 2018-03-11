import logging
import telegram
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove
from universitybot.translation import translate


class Links:
    """
    Help a user by listing the bot functionalities.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler("links", links))

        logger.info("Added /links command to Telegram handler")

'''
COMMAND VARIABLES
'''
# Utility
logger = logging.getLogger(__name__)

'''
COMMANDS
'''


@translate
def links(bot, update):
    user = update.message.from_user

    logger.info("%s[%s] started links command: %s" % (user.first_name, user['language_code'], update.message.text))

    link_list =     [
        {
            'category_name': _('Bureaucracy'),
            'links': [
                (_('Registrar\'s Office'), 'https://www.polimi.it/studenti-iscritti/contatti/sportelli-e-uffici-aperti-agli-studenti/'),
                (_('Career Service'), 'http://www.careerservice.polimi.it/it-IT/Home/Index/')]
        },
        {
            'category_name': _('Online accounts'),
            'links': [
                (_('Online Services'), 'https://www.polimi.it/servizionline/'),
                (_('Office 365'), 'https://outlook.office365.com/polimi.it'),
                (_('Beep'), 'https://beep.metid.polimi.it/')]
        },
        {
            'category_name': _('Programmes'),
            'links': [
                (_('Degree Programmes'),
                 'https://www4.ceda.polimi.it/manifesti/manifesti/controller/ManifestoPublic.do'),
                (_('Bachelor of Science list'), 'https://www.polimi.it/corsi/corsi-di-laurea/'),
                (_('Master of Science list'), 'https://www.polimi.it/corsi/corsi-di-laurea-magistrale/'),
                (_('Academic Calendar'), 'https://www.polimi.it/studenti-iscritti/calendario-e-scadenze/')]
        },
        {
            'category_name': _('Social'),
            'links': [
                (_('Facebook Official Page'), 'https://www.facebook.com/polimi/'),
                (_('Facebook Official Group'), 'https://www.facebook.com/groups/groupsatpolimilano/')]
        }
    ]

    link_string = ''
    for category in link_list:
        link_string += '\n\n*{}*'.format(category['category_name'])
        for link in category['links']:
            link_string += '\n[{}]({})'.format(link[0], link[1])

    update.message.reply_text(_('Useful links for Politecnico di Milano:') + link_string,
                              disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=telegram.ParseMode.MARKDOWN)
