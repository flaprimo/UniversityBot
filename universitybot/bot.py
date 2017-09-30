from universitybot.commands.start import Start
from universitybot.commands.info import Info
from universitybot.commands.help import Help
from universitybot.commands.freeclassrooms import FreeClassrooms

from telegram.ext import Updater


class Bot:
    def __init__(self, conf):
        self.conf = conf

        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(self.conf['token'])

        # Get the dispatcher and register handlers
        self.dispatcher = self.updater.dispatcher

        self._add_commands()

        # Start the Bot
        if self.conf['connection'] == 'webhook':
            self._start_webhook()
        else:
            self._start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def _start_webhook(self):
        self.updater.start_webhook(
            listen=self.conf['webhook']['ip'],  # '0.0.0.0'
            port=self.conf['webhook']['port'],  # 8443
            url_path=self.conf['token'],
            key=self.conf['webhook']['key'],  # 'private.key'
            cert=self.conf['webhook']['cert'],  # 'cert.pem'
            webhook_url='{}:{}/{}'.format(self.conf['webhook']['url'],
                                          self.conf['webhook']['port'],
                                          self.conf['token']))  # 'https://example.com:8443/TOKEN'

    def _start_polling(self):
        self.updater.start_polling()

    def _add_commands(self):
        Start(self.dispatcher)
        Info(self.dispatcher)
        Help(self.dispatcher)
        FreeClassrooms(self.dispatcher)

    '''
    def error(bot, update, error):
        logging.warning('Update "%s" caused error "%s"' % (update, error))
    '''