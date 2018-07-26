import datetime
import gettext
import logging
from itertools import groupby

import telegram
from requests.exceptions import RequestException
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, RegexHandler, ConversationHandler

from bot.poli_api.poli_api import PolimiAPI

'''
COMMAND VARIABLES
'''
# Utility
logger = logging.getLogger(__name__)

# Conversation FSM
STARTTIME_HOUR, STARTTIME_MIN, ENDTIME_HOUR, ENDTIME_MIN, DAY = range(5)  # conversation states

# Keyboard
hour_keyboard = [['08', '09', '10', '11', '12', '13'],
                 ['14', '15', '16', '17', '18', '19']]  # hours of the day

minute_keyboard = [['00', '15', '30', '45']]  # quarter of minutes

day_keyboard = [['today', 'tomorrow']]  # days

# Regex
hour_regex = '^(08|09|1[0-9])$'

minute_regex = '^(00|15|30|45)$'

day_regex = '^(today|tomorrow)$'


class FreeClassrooms:
    """
    Show free available classrooms.
    """

    def __init__(self, dispatcher):
        # Add conversation handler with the FSM states to the dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('freeclassrooms', self.freeclassrooms)],

            states={
                STARTTIME_HOUR: [RegexHandler(hour_regex, self.select_starttime_hour, pass_user_data=True)],

                STARTTIME_MIN: [RegexHandler(minute_regex, self.select_starttime_min, pass_user_data=True)],

                ENDTIME_HOUR: [RegexHandler(hour_regex, self.select_endtime_hour, pass_user_data=True)],

                ENDTIME_MIN: [RegexHandler(minute_regex, self.select_endtime_min, pass_user_data=True)],

                DAY: [RegexHandler(day_regex, self.select_day, pass_user_data=True)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel, pass_user_data=True)]
        )

        dispatcher.add_handler(conv_handler)

        logger.info("Added /freeclassrooms command to Telegram handler")

    @staticmethod
    def freeclassrooms(bot, update):
        user = update.message.from_user

        logger.debug("%s[%s] started freeclassroom command: %s" %
                     (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Let\'s search for free classrooms!\n\nSelect start time hour')
        reply_keyboard = ReplyKeyboardMarkup(hour_keyboard, one_time_keyboard=True, resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_keyboard)

        return STARTTIME_HOUR

    @staticmethod
    def select_starttime_hour(bot, update, user_data):
        user = update.message.from_user
        user_data['starttime_hour'] = update.message.text

        logger.debug("%s[%s] added starttime_hour: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Select start time minutes')
        reply_keyboard = ReplyKeyboardMarkup(minute_keyboard, one_time_keyboard=True, resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_keyboard)

        return STARTTIME_MIN

    @staticmethod
    def select_starttime_min(bot, update, user_data):
        user = update.message.from_user
        user_data['starttime_min'] = update.message.text

        logger.debug("%s[%s] added starttime_min: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Select end time hour')
        reply_keyboard = ReplyKeyboardMarkup(hour_keyboard, one_time_keyboard=True, resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_keyboard)

        return ENDTIME_HOUR

    @staticmethod
    def select_endtime_hour(bot, update, user_data):
        user = update.message.from_user
        user_data['endtime_hour'] = update.message.text

        logger.debug("%s[%s] added endtime_hour: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Select end time minutes')
        reply_keyboard = ReplyKeyboardMarkup(minute_keyboard, one_time_keyboard=True, resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_keyboard)

        return ENDTIME_MIN

    @staticmethod
    def select_endtime_min(bot, update, user_data):
        user = update.message.from_user
        user_data['endtime_min'] = update.message.text

        logger.debug("%s[%s] added endtime_min: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Select day')
        reply_keyboard = ReplyKeyboardMarkup(day_keyboard, one_time_keyboard=True, resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=reply_keyboard)

        return DAY

    @staticmethod
    def select_day(bot, update, user_data):
        user = update.message.from_user
        user_data['day'] = update.message.text

        # get the day
        date = datetime.date.today()
        if user_data['day'] == 'tomorrow':
            date += datetime.timedelta(days=1)

        # get the time
        start_time = datetime.time(int(user_data['starttime_hour']), int(user_data['starttime_min']))
        end_time = datetime.time(int(user_data['endtime_hour']), int(user_data['endtime_min']))

        logger.debug("%s[%s] added day: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        if end_time > start_time:

            logger.debug("%s[%s] completed successfully /classroom command" % (user.first_name, user['language_code']))

            try:
                # TODO do for all campuses
                freeclassrooms_json = PolimiAPI.get_elenco_aule_libere('MIA', date, start_time, end_time)
            except RequestException:
                reply = translation.gettext('Sorry, Politecnico di Milano server seems not responding\nTry again later')
                bot.send_message(chat_id=update.message.chat_id, text=reply)
                user_data.clear()
                return ConversationHandler.END

            classroom_type_filter = ['DEPARTMENTAL CLASSROOM', 'CONFERENCE ROOM', 'AUDITORIUM', 'MASTER CLASSROOM']

            # get tuple list of classrooms
            classroom_list = []
            for classroom in freeclassrooms_json:
                if classroom['categoria'] not in classroom_type_filter:
                    (location, address) = classroom['dove'].split(', ')
                    classroom_list.append((address, classroom['sigla']))

            # group classrooms by address
            classrooms = []
            for address, classroom_names in groupby(classroom_list, lambda x: x[0]):
                names_list = []
                for classroom_name in classroom_names:
                    names_list.append(classroom_name[1])
                classrooms.append((address, names_list))

            free_classrooms = classrooms_to_string(classrooms)

            reply = translation.gettext('Free classrooms for *%s %s* from *%s* to *%s* are:\n%s' %
                                        (user_data['day'], date.strftime('%Y-%m-%d'), start_time.strftime('%H:%M'),
                                         end_time.strftime('%H:%M'), free_classrooms))

            bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=ReplyKeyboardRemove(),
                             parse_mode=telegram.ParseMode.MARKDOWN)

        else:

            reply = translation.gettext('I\'m sorry, but it seems like you didn\'t enter an end time which is greater '
                                        'than the start time')
            bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=ReplyKeyboardRemove())

        # delete user conversation data
        user_data.clear()

        return ConversationHandler.END

    @staticmethod
    def cancel(bot, update, user_data):
        user = update.message.from_user

        logger.debug("%s[%s canceled command: %s" % (user.first_name, user['language_code'], update.message.text))

        translation = gettext.translation('strings', '../locale', languages=[user['language_code']], fallback=True)

        reply = translation.gettext('Bye! I hope we can talk again some day.')

        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_markup=ReplyKeyboardRemove())

        # delete user conversation data
        user_data.clear()

        return ConversationHandler.END


def classrooms_to_string(freeclassrooms_list):
    freeclassrooms_string = ''

    for address in freeclassrooms_list:
        freeclassrooms_string += "*{}*\n".format(address[0])
        for classroom in address[1]:
            freeclassrooms_string += "   {}\n".format(classroom)
        freeclassrooms_string += "\n"

    return freeclassrooms_string
