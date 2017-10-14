#!/usr/bin/env python3

import logging
import json
from universitybot.bot import Bot


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    #filename='log.log'
                    )

logger = logging.getLogger(__name__)


def main():
    # Load configuration file
    with open('conf/conf.json') as json_data_file:
        conf = json.load(json_data_file)
    logger.info("Configuration file loaded")

    # run bot
    Bot(conf['telegram'])


if __name__ == '__main__':
    main()
