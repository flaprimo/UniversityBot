#!/usr/bin/env python3

import argparse
import json
import logging
from datetime import time
from logging.handlers import TimedRotatingFileHandler

from bot.bot import Bot

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(format=log_format)

root_logger = logging.getLogger()

version = '0.1 alpha'


def read_config():
    config = None

    try:
        with open('config/config.json') as f:
            config = json.load(f)
            if config['telegram']['token'] is not '':
                root_logger.debug('Token: ' + config['telegram']['token'])
            else:
                root_logger.warning('Token not found in config file')
                root_logger.debug('Connection type: ' + config['telegram']['connection'])
            if config['telegram']['connection'] == 'webhook':
                root_logger.debug('Webhook ip: ' + config['telegram']['webhook']['ip'])
                root_logger.debug('Webhook port: ' + config['telegram']['webhook']['port'])
                root_logger.debug('Webhook key: ' + config['telegram']['webhook']['key'])
                root_logger.debug('Webhook cert: ' + config['telegram']['webhook']['cert'])
                root_logger.debug('Webhook url: ' + config['telegram']['webhook']['url'])
                root_logger.info('Configuration successfully loaded')
    except FileNotFoundError:
        root_logger.error("No config file found!")
    finally:
        return config


def main():
    parser = argparse.ArgumentParser(prog='polibot')

    parser.add_argument('--logfile', action='store_const', const='logs/bot.log',
                        help='custom location for the log file')
    parser.add_argument('--loglevel', help='changes the default log level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-v', '--version', action='version', version='%(prog)s' + version)

    args = parser.parse_args()

    if args.logfile is not None:
        rh = TimedRotatingFileHandler(args.logfile, when='W5', backupCount=9, atTime=time(hour=0, minute=0, second=0))
    else:
        rh = TimedRotatingFileHandler('logs/bot.log', when='W5', backupCount=9, atTime=time(hour=0, minute=0, second=0))

    if args.loglevel is not None:
        rh.setLevel(args.loglevel)
        root_logger.setLevel(args.loglevel)
    else:
        rh.setLevel('INFO')
        root_logger.setLevel('INFO')

    formatter = logging.Formatter(log_format)
    rh.setFormatter(formatter)

    root_logger.addHandler(rh)

    config = read_config()

    root_logger.info(config['telegram']['token'])

    try:
        bot = Bot(config['telegram'])
        bot.updater.idle()
    except TypeError:
        root_logger.critical("No token found! Have you created config.json in ./bot/config/ ?")


if __name__ == '__main__':
    main()
