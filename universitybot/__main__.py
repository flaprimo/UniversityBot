#!/usr/bin/env python3

import logging.config
import json
from universitybot.bot import Bot


def main():
    # load log configuration file
    with open('conf/logging.json') as json_data_file:
        logging_json = json.load(json_data_file)
    logging.config.dictConfig(logging_json)

    logger = logging.getLogger(__name__)

    # load bot configuration file
    with open('conf/conf.json') as json_data_file:
        conf = json.load(json_data_file)
    logger.info("Configuration file loaded")

    # run bot
    Bot(conf['telegram'])


if __name__ == '__main__':
    main()
