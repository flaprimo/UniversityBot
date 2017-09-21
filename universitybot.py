#!/usr/bin/env python3

import json
import logging
from telegram.ext import Updater
from universitybot.commands.start import Start
from universitybot.commands.help import Help
from universitybot.commands.info import Info
from universitybot.commands.freeclassrooms import FreeClassrooms

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # filename='log.log'
                    )

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Load configuration file
    with open('conf/conf.test.json') as json_data_file:
        conf = json.load(json_data_file)

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(conf["telegram"]["token"])

    # Get the dispatcher and register handlers
    dispatcher = updater.dispatcher

    Start(dispatcher)
    Help(dispatcher)
    Info(dispatcher)
    FreeClassrooms(dispatcher)

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()