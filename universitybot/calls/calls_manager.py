from datetime import timedelta
from universitybot.calls.cache import Cache
import json
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
        return _pycurl_call(url)


def _requests_call(url):
    import requests

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


def _pycurl_call(url):
    import pycurl
    from io import BytesIO

    buffer = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 8)
    c.setopt(c.COOKIEFILE, '')
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Accept-Charset: UTF-8'])
    c.setopt(c.WRITEFUNCTION, buffer.write)

    try:
        c.perform()

        response_json = json.loads(buffer.getvalue().decode('utf-8'))
        buffer.close()
        logger.debug('Response not cached')

        # update cache
        _cache.update_cache(url, response_json)

        return response_json
    except pycurl.error:
        buffer.close()
        logger.error('Reponse not cached error')
