import logging
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, RegexHandler, MessageHandler
from telegram.ext.filters import Filters
from universitybot.providers.classroominfo import ClassroomInfoProvider
from universitybot.translation import translate


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
            entry_points=[CommandHandler("classinfo", classinfo)],
            states={
                UNIVERSITY_CAMPUS: [RegexHandler(campus_regexp, select_campus, pass_user_data=True)],
                CLASSROOM_NAME: [MessageHandler(Filters.text, select_classroom, pass_user_data=True)],
                CLASSROOM_INFO: [RegexHandler(class_details_regexp, classroom_details, pass_user_data=True)]
            },
            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )

        dispatcher.add_handler(conv_handler)

        logger.info("Added /classinfo command to Telegram handler")


logger = logging.getLogger(__name__)

UNIVERSITY_CAMPUS, CLASSROOM_NAME, CLASSROOM_INFO = range(3)

campuses_codes = {}
campuses_list = []
campus_regexp = '^('
class_details_regexp = '^(Building|Photo|Notes|How to reach it)$'


def classinfo(bot, update):
    user = update.message.from_user

    reply_keyboard = list(chunks(campuses_list, 4))

    logger.info("{}[{}] started classinfo command: {}".format(user.first_name, user['language_code'], update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Select a campus'),
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return UNIVERSITY_CAMPUS


def select_campus(bot, update, user_data):
    user = update.message.from_user
    for campus in campuses_codes:
        if campuses_codes[campus] == update.message.text:
            user_data['campus_code'] = campus

    logger.info('{} selected campus {}'.format(user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('In which classroom are you interest about?'))

    return CLASSROOM_NAME


def select_classroom(bot, update, user_data):
    user = update.message.from_user
    user_data['classroom_info'] = update.message.text

    logger.info('{} selected classroom {}'.format(user.first_name, update.message.text))

    classroom_dict = ClassroomInfoProvider.get_campus_classroom(user_data['campus_code'])

    for classroom in classroom_dict:
        if re.sub('\(.*\)','',classroom['sigla']).replace('_LABORATORIO', '').replace('.', '').lower() == \
                re.sub('\(.*\)', '', update.message.text).replace('_LABORATORIO', '').replace('.', '').lower():

            user_data['class_id'] = classroom['id_aula']

            reply_keyboard = [['Building', 'Photo', 'Notes'], ['How to reach it']]
            translate(user['language_code'])
            update.message.reply_text(_('Classroom found!\nWhat do you want to know?'),
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return CLASSROOM_INFO
    logger.warning('{} selected classroom {} that doesn\'t exists'.format(user.first_name, update.message.text))
    update.message.reply_text(_('Classroom not found, try again or /cancel'))
    return CLASSROOM_NAME


def classroom_details(bot, update, user_data):
    user = update.message.from_user
    logger.info('{} selected {} info'.format(user.first_name, update.message.text))
    classroom_detail = ClassroomInfoProvider.get_classroom_details(user_data['class_id'])

    pass


def cancel(bot, update, user_data):
    user = update.message.from_user

    logger.info("{} canceled command: {}".format(user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Bye! I hope we can talk again some day.'), reply_markup=ReplyKeyboardRemove())

    # delete user conversation data
    _delete_userdata(user_data)

    return ConversationHandler.END


'''
UTILITIES
'''


def create_campus_regexp(campuses):
    global campus_regexp
    for campus in campuses:
        campus_regexp = campus_regexp + campus + '|'
    campus_regexp = campus_regexp[:-1] + ')$'


def chunks(campuses, max_col):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(campuses), max_col):
        yield campuses[i:i + max_col]


def _delete_userdata(user_data):
    if 'campus_code' in user_data:
        del user_data['campus_code']

    if 'classroom_info' in user_data:
        del user_data['classroom_info']

    if 'class_id' in user_data:
        del user_data['class_id']
