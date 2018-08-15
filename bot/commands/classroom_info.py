import gettext
import logging
from datetime import timedelta
from re import sub

from requests.exceptions import RequestException
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import CommandHandler, ConversationHandler, RegexHandler, MessageHandler
from telegram.ext.filters import Filters

from bot.poli_api.poli_api import PolimiAPI
from bot.utility.utility import chunks

logger = logging.getLogger(__name__)

campuses_codes = {}
campuses_list = []
campus_regexp = '^('
class_details_regexp = '^(Building|Photo|Notes|Directions|Cancel)$'

UNIVERSITY_CAMPUS, CLASSROOM_NAME, CLASSROOM_DETAILS = range(3)


class ClassroomInfo:
    """
    Returns info for a given classroom
    """

    def __init__(self, dispatcher):
        try:
            global campuses_list
            campuses_json = PolimiAPI.get_elenco_sedi()

            for campus in campuses_json:
                if campus['csis'] not in ['all']:
                    campuses_codes[campus['csis']] = campus['desc_sede']

            for key in campuses_codes:
                campuses_list.append(campuses_codes[key])
            create_campus_regexp(campuses_list)

        except RequestException:
            logger.error('Politecnico di Milano server seems not responding')
            logger.error('Can\'t initialize classroominfo')
            raise RequestException
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("classroominfo", self.classroom_info)],
            states={UNIVERSITY_CAMPUS: [RegexHandler(campus_regexp, self.select_campus, pass_user_data=True)],
                    CLASSROOM_NAME: [MessageHandler(Filters.text, self.select_classroom, pass_user_data=True)],
                    CLASSROOM_DETAILS: [RegexHandler(class_details_regexp, self.classroom_details, pass_user_data=True)]
                    },
            fallbacks=[CommandHandler('cancel', self.cancel, pass_user_data=True)],
            conversation_timeout=timedelta(minutes=5)
        )

        dispatcher.add_handler(conv_handler)

        logger.info('Added /classroominfo command to Telegram handler')

    @staticmethod
    def classroom_info(bot, update):
        user = update.message.from_user

        logger.debug("%s[%s] started classroominfo command: %s" % (user.first_name, user['language_code'],
                                                                   update.message.text))

        translation = gettext.translation('strings', 'bot/locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Select a campus')

        reply_keyboard = ReplyKeyboardMarkup(list(chunks(campuses_list, 4)), one_time_keyboard=True,
                                             resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_keyboard)

        return UNIVERSITY_CAMPUS

    @staticmethod
    def select_campus(bot, update, user_data):
        user = update.message.from_user

        logger.debug('%s[%s] selected campus %s' % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', 'bot/locale', languages=[user['language_code']], fallback=True)

        for campus in campuses_codes:
            if campuses_codes[campus] == update.message.text:
                user_data['campus_code'] = campus

        reply = translation.gettext('What classroom are you interested in?')
        bot.send_message(chat_id=update.message.chat_id, text=reply)
        return CLASSROOM_NAME

    @staticmethod
    def select_classroom(bot, update, user_data):
        user = update.message.from_user
        user_data['classroom_info'] = update.message.text

        logger.debug('%s[%s] selected classroom %s' % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', 'bot/locale', languages=[user['language_code']], fallback=True)

        try:
            classroom_dict = PolimiAPI.get_elenco_aule(user_data['campus_code'])
        except RequestException:
            reply = translation.gettext('Sorry, Politecnico di Milano server seems not responding\nTry again later')
            bot.send_message(chat_id=update.message.chat_id, text=reply)
            user_data.clear()
            return ConversationHandler.END

        for classroom in classroom_dict:
            if strip_classroom_name(classroom['sigla']) == strip_classroom_name(update.message.text):
                user_data['class_id'] = classroom['id_aula']

                reply_keyboard = [['Building', 'Directions'], ['Notes', 'Photo'], ['Cancel']]
                reply = translation.gettext('Classroom found!\nWhat do you want to know?')

                bot.send_message(chat_id=update.message.chat_id, text=reply,
                                 reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
                return CLASSROOM_DETAILS

        logger.warning('%s[%s] selected classroom %s that doesn\'t exists' % (user.first_name, user['language_code'],
                                                                              update.message.text))
        update.message.reply_text(translation.gettext('Classroom not found, try again or /cancel'))

        return CLASSROOM_NAME

    @staticmethod
    def classroom_details(bot, update, user_data):
        user = update.message.from_user
        option_selected = update.message.text
        logger.debug('%s[%s] selected %s info' % (user.first_name, user['language_code'], option_selected))

        translation = gettext.translation('strings', 'bot/locale', languages=[user['language_code']], fallback=True)

        reply = ''

        try:
            classroom_detail = PolimiAPI.get_dettaglio_aula(user_data['class_id'])
        except RequestException:
            reply = translation.gettext('Sorry, Politecnico di Milano server seems not responding\nTry again later')
            bot.send_message(chat_id=update.message.chat_id, text=reply)
            user_data.clear()
            return ConversationHandler.END

        if option_selected == 'Building':
            reply = translation.gettext('The Classroom you selected is in %s at %s floor' %
                                        (classroom_detail['nomeEdificio'], classroom_detail['nomePiano']))

        elif option_selected == 'Photo':
            url = classroom_detail['url_foto_aula']
            photo = PolimiAPI.get_photo(user_data['class_id'], url)
            with open(photo, 'rb') as f:
                bot.send_photo(chat_id=update.message.chat_id, photo=f,
                               caption=translation.gettext('Here\'s the photo of the classroom'))

        elif option_selected == 'Notes':
            reply = classroom_detail['noteAccessoEdificio']

        elif option_selected == 'Directions':
            access_ways = classroom_detail['percorsiAccesso']

            reply = ''
            for way in access_ways:
                reply += translation.gettext('*From %s* \n \t %s\n' % (way['partenza'], way['descrizione']))
        elif option_selected == 'Cancel':
            ClassroomInfo.cancel(bot, update, user_data)

        if reply is not '':
            bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=ParseMode.MARKDOWN)

        return CLASSROOM_DETAILS

    @staticmethod
    def cancel(bot, update, user_data):
        user = update.message.from_user

        logger.debug("%s[%s canceled command: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', 'bot/locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Bye! I hope we can talk again some day.')

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=ReplyKeyboardRemove())

        # delete user conversation data
        user_data.clear()

        return ConversationHandler.END


'''
UTILITIES
'''


def create_campus_regexp(campuses):
    global campus_regexp
    for campus in campuses:
        campus_regexp = campus_regexp + campus + '|'
    campus_regexp = campus_regexp[:-1] + ')$'


def strip_classroom_name(classroom_name):
    return sub('\(.*\)', '', classroom_name).replace('_LABORATORIO', '').replace('.', '').lower()
