import logging

from telegram.ext import Updater

from bot.commands.classroom_info import ClassroomInfo
from bot.commands.credits import Credits
from bot.commands.free_classrooms import FreeClassrooms
from bot.commands.help import Help
from bot.commands.links import Links
from bot.commands.start import Start

logger = logging.getLogger(__name__)


class Bot:

    def __init__(self, conf):
        self.conf = conf
        self.updater = Updater(token=self.conf['token'])
        self.dispatcher = self.updater.dispatcher

        self.add_commands()

        if self.conf['connection'] == 'webhook':
            self.start_webhook()
        else:
            self.start_polling()

    def start_polling(self):
        self.updater.start_polling()
        logger.info("Polling started")

    def start_webhook(self):
        raise NotImplementedError

    def add_commands(self):
        Start(self.dispatcher)
        Links(self.dispatcher)
        Help(self.dispatcher)
        Credits(self.dispatcher)
        ClassroomInfo(self.dispatcher)
        FreeClassrooms(self.dispatcher)
        logger.info('Added all commands to bot')
