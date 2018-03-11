import logging
import re
from universitybot.utility import chunks, delete_userdata
from universitybot.translation import translate
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler, CommandHandler, RegexHandler, MessageHandler
from telegram.ext.filters import Filters
from universitybot.providers.classroominfo import ClassroomInfoProvider


class ClassroomInfo:
    """
    Returns info for a given classroom
    """
    def __init__(self, dispatcher):
        global campuses_list
        campuses_codes.update(ClassroomInfoProvider.get_campuses())
        for key in campuses_codes:
            campuses_list.append(campuses_codes[key])
        create_campus_regexp(campuses_list)

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("classroominfo", classroominfo)],
            states={
                UNIVERSITY_CAMPUS: [RegexHandler(campus_regexp, select_campus, pass_user_data=True)],
                CLASSROOM_NAME: [MessageHandler(Filters.text, select_classroom, pass_user_data=True)],
                CLASSROOM_INFO: [RegexHandler(class_details_regexp, classroom_details, pass_user_data=True)]
            },
            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )

        dispatcher.add_handler(conv_handler)

        logger.info("Added /classroominfo command to Telegram handler")


logger = logging.getLogger(__name__)

UNIVERSITY_CAMPUS, CLASSROOM_NAME, CLASSROOM_INFO = range(3)

campuses_codes = {}
campuses_list = []
campus_regexp = '^('
class_details_regexp = '^(Building|Photo|Notes|Directions|Cancel)$'


@translate
def classroominfo(bot, update):
    user = update.message.from_user

    reply_keyboard = list(chunks(campuses_list, 4))

    logger.info("{}[{}] started classroominfo command: {}".format(user.first_name, user['language_code'], update.message.text))

    update.message.reply_text(_('Select a campus'),
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return UNIVERSITY_CAMPUS


@translate
def select_campus(bot, update, user_data):
    user = update.message.from_user
    for campus in campuses_codes:
        if campuses_codes[campus] == update.message.text:
            user_data['campus_code'] = campus

    logger.info('{} selected campus {}'.format(user.first_name, update.message.text))

    update.message.reply_text(_('What classroom are you interested in?'))

    return CLASSROOM_NAME


@translate
def select_classroom(bot, update, user_data):
    user = update.message.from_user
    user_data['classroom_info'] = update.message.text

    logger.info('{} selected classroom {}'.format(user.first_name, update.message.text))

    classroom_dict = ClassroomInfoProvider.get_campus_classroom(user_data['campus_code'])

    for classroom in classroom_dict:
        if strip_classroom_name(classroom['sigla']) == strip_classroom_name(update.message.text):

            user_data['class_id'] = classroom['id_aula']

            reply_keyboard = [['Building', 'Directions'], ['Notes', 'Photo'], ['Cancel']]

            update.message.reply_text(_('Classroom found!\nWhat do you want to know?'),
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return CLASSROOM_INFO

    logger.warning('{} selected classroom {} that doesn\'t exists'.format(user.first_name, update.message.text))
    update.message.reply_text(_('Classroom not found, try again or /cancel'))

    return CLASSROOM_NAME


@translate
def classroom_details(bot, update, user_data):
    user = update.message.from_user
    option_selected = update.message.text
    logger.info('{} selected {} info'.format(user.first_name, option_selected))

    classroom_detail = ClassroomInfoProvider.get_classroom_details(user_data['class_id'])

    if option_selected == 'Building':
        update.message.reply_text(_('The Classroom you selected is in ') + classroom_detail['nomeEdificio'] +
                                  _(' at ') + classroom_detail['nomePiano'] + _(' floor.'))

    elif option_selected == 'Photo':
        update.message.reply_text(_('Here\'s the photo of the classroom: ') + classroom_detail['url_foto_aula'])

    elif option_selected == 'Notes':
        update.message.reply_text(classroom_detail['noteAccessoEdificio'])

    elif option_selected == 'Directions':
        access_ways = classroom_detail['percorsiAccesso']

        response = ''
        for way in access_ways:
            response += '*' + _('From') + ' {}* \n \t {}\n'.format(way['partenza'], way['descrizione'])

        update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

    else:
        cancel(bot, update, user_data)
        return ConversationHandler.END

    return CLASSROOM_INFO


@translate
def cancel(bot, update, user_data):
    user = update.message.from_user

    logger.info("{} canceled command: {}".format(user.first_name, update.message.text))

    update.message.reply_text(_('Bye! I hope we can talk again some day.'), reply_markup=ReplyKeyboardRemove())

    # delete user conversation data
    delete_userdata(user_data, ['campus_code', 'classroom_info', 'class_id'])

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
    return re.sub('\(.*\)', '', classroom_name).replace('_LABORATORIO', '').replace('.', '').lower()
