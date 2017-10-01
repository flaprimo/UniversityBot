from datetime import timedelta
from universitybot.calls.cache import Cache
import json
import requests
import logging

logger = logging.getLogger(__name__)
_cache = Cache()


def call(url, payload='', delta_time=timedelta(hours=24)):
    if payload != '':
        url = url + '?' + payload
    logger.debug('Handle API call for: %s' % url)

    cached = _cache.get_cached(url, delta_time)

    if cached is not None:
        logger.debug('Response cached')
        # return cached content
        return cached
    else:
        # make api call because not found in cache
        response = requests.get(url)

        if response.ok:
            response_json = json.loads(response.text)
            logger.debug('Response not cached')

            # update cache
            _cache.update_cache(url, response_json)

            return response_json
        else:
            logger.error('Reponse not cached error')
            response.raise_for_status()