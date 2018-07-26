import gettext
import logging

import telegram
from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)


class Links:
    """
    Help a user by listing the bot functionalities.
    """

    def __init__(self, dispatcher):
        # Add command to the dispatcher
        dispatcher.add_handler(CommandHandler('links', self.links))

        logger.info('Added /links command to Telegram handler')

    @staticmethod
    def links(bot, update):
        user = update.message.from_user

        logger.debug('%s[%s] started links command: %s' % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        link_list = [
            {
                'category_name': translation.gettext('Bureaucracy'),
                'links': [
                    (translation.gettext('Registrar\'s Office'),
                     'https://www.polimi.it/studenti-iscritti/contatti/sportelli-e-uffici-aperti-agli-studenti/'),
                    (translation.gettext('Career Service'), 'http://www.careerservice.polimi.it/it-IT/Home/Index/')]
            },
            {
                'category_name': translation.gettext('Online accounts'),
                'links': [
                    (translation.gettext('Online Services'), 'https://www.polimi.it/servizionline/'),
                    (translation.gettext('Office 365'), 'https://outlook.office365.com/polimi.it'),
                    (translation.gettext('Beep'), 'https://beep.metid.polimi.it/')]
            },
            {
                'category_name': translation.gettext('Programmes'),
                'links': [
                    (translation.gettext('Degree Programmes'),
                     'https://www4.ceda.polimi.it/manifesti/manifesti/controller/ManifestoPublic.do'),
                    (translation.gettext('Bachelor of Science list'), 'https://www.polimi.it/corsi/corsi-di-laurea/'),
                    (translation.gettext('Master of Science list'),
                     'https://www.polimi.it/corsi/corsi-di-laurea-magistrale/'),
                    (translation.gettext('Academic Calendar'),
                     'https://www.polimi.it/studenti-iscritti/calendario-e-scadenze/')]
            },
            {
                'category_name': translation.gettext('Social'),
                'links': [
                    (translation.gettext('Facebook Official Page'), 'https://www.facebook.com/polimi/'),
                    (translation.gettext('Facebook Official Group'),
                     'https://www.facebook.com/groups/groupsatpolimilano/')]
            }
        ]

        reply = ''
        for category in link_list:
            reply += '\n\n*%s*' % category['category_name']
            for link in category['links']:
                reply += '\n[%s](%s)' % (link[0], link[1])

        reply = translation.gettext('Useful links for Politecnico di Milano:') + reply

        bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=telegram.ParseMode.MARKDOWN)
