import datetime
import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, RegexHandler, ConversationHandler)
from lib.FreeClassrooms.FreeClassroomsPolimi import FreeClassroomsPolimi
from lib.Translation import translate


class FreeClassrooms:
    """
    Show free available classrooms.
    """

    def __init__(self, dispatcher):
        # Add conversation handler with the FSM states to the dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('freeclassrooms', freeclassrooms)],

            states={
                STARTTIME_HOUR: [RegexHandler(hour_regex, select_starttime_hour, pass_user_data=True)],

                STARTTIME_MIN: [RegexHandler(minute_regex, select_starttime_min, pass_user_data=True)],

                ENDTIME_HOUR: [RegexHandler(hour_regex, select_endtime_hour, pass_user_data=True)],

                ENDTIME_MIN: [RegexHandler(minute_regex, select_endtime_min, pass_user_data=True)],

                DAY: [RegexHandler(day_regex, select_day, pass_user_data=True)]
            },

            fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
        )

        dispatcher.add_handler(conv_handler)

        logger.info("Added FreeClassrooms command to Telegram handler")


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


'''
COMMANDS
'''


def freeclassrooms(bot, update):
    user = update.message.from_user
    reply_keyboard = hour_keyboard

    logger.info("%s[%s] started freeclassroom command: %s" % (user.first_name, user['language_code'], update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Let\'s search for free classrooms!\nSelect start time hour'),
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STARTTIME_HOUR


def select_starttime_hour(bot, update, user_data):
    user = update.message.from_user
    user_data['starttime_hour'] = update.message.text

    logger.info("%s added starttime_hour: %s" % (user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Select start time minutes'),
                              reply_markup=ReplyKeyboardMarkup(minute_keyboard, one_time_keyboard=True))

    return STARTTIME_MIN


def select_starttime_min(bot, update, user_data):
    user = update.message.from_user
    user_data['starttime_min'] = update.message.text

    logger.info("%s added starttime_min: %s" % (user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Select end time hour'),
                              reply_markup=ReplyKeyboardMarkup(hour_keyboard, one_time_keyboard=True))

    return ENDTIME_HOUR


def select_endtime_hour(bot, update, user_data):
    user = update.message.from_user
    user_data['endtime_hour'] = update.message.text

    logger.info("%s added endtime_hour: %s" % (user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Select end time minutes'),
                              reply_markup=ReplyKeyboardMarkup(minute_keyboard, one_time_keyboard=True))

    return ENDTIME_MIN


def select_endtime_min(bot, update, user_data):
    user = update.message.from_user
    user_data['endtime_min'] = update.message.text

    logger.info("%s added endtime_min: %s" % (user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Select day'),
                              reply_markup=ReplyKeyboardMarkup(day_keyboard, one_time_keyboard=True))

    return DAY


def select_day(bot, update, user_data):
    user = update.message.from_user
    user_data['day'] = update.message.text

    # get the day
    day = datetime.date.today()
    if user_data['day'] == 'tomorrow':
        day += datetime.timedelta(days=1)

    # get the time
    starttime = datetime.time(int(user_data['starttime_hour']), int(user_data['starttime_min']))
    endtime = datetime.time(int(user_data['endtime_hour']), int(user_data['endtime_min']))

    logger.info("%s added day: %s" % (user.first_name, update.message.text))
    translate(user['language_code'])

    if endtime > starttime:
        try:
            free_classrooms = FreeClassroomsPolimi.get_free_classrooms(day, starttime, endtime)

            update.message.reply_text(_('Free classrooms for *') + user_data['day'] + ' ' + day.strftime('%Y-%m-%d') +
                                      _('* from *') + starttime.strftime('%H:%M') +
                                      _('* to *') + endtime.strftime('%H:%M') +
                                      _('* are:\n') + free_classrooms,
                                      reply_markup=ReplyKeyboardRemove(),
                                      parse_mode=telegram.ParseMode.MARKDOWN)

        except:
            logger.error("Politecnico di Milano server seems not responding")

            update.message.reply_text(_('I\'m sorry, but it seems like Politecnico has some difficulties, ') +
                                      _('not my fault! (pinky swear)'),
                                      reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text(_('I\'m sorry, but it seems like you didn\'t enter an end time which is') +
                                  _(' greater than the start time, not my fault!'),
                                  reply_markup=ReplyKeyboardRemove())

    # delete user conversation data
    _delete_userdata(user_data)

    return ConversationHandler.END


def cancel(bot, update, user_data):
    user = update.message.from_user

    logger.info("%s canceled command: %s" % (user.first_name, update.message.text))

    translate(user['language_code'])
    update.message.reply_text(_('Bye! I hope we can talk again some day.'), reply_markup=ReplyKeyboardRemove())

    # delete user conversation data
    _delete_userdata(user_data)

    return ConversationHandler.END


'''
UTILITIES
'''


def _delete_userdata(user_data):
    if 'starttime_hour' in user_data:
        del user_data['starttime_hour']

    if 'starttime_min' in user_data:
        del user_data['starttime_min']

    if 'endtime_hour' in user_data:
        del user_data['endtime_hour']

    if 'endtime_min' in user_data:
        del user_data['endtime_min']

    if 'day' in user_data:
        del user_data['day']
