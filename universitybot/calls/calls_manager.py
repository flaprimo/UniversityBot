import json
import requests
from datetime import timedelta
from universitybot.calls.cache import Cache

_cache = Cache()


def call(url, payload='', delta_time=timedelta(hours=24)):
    if payload != '':
        url = url + '?' + payload

    cached = _cache.get_cached(url, delta_time)

    if cached is not None:
        # return cached content
        return cached[0]['content']
    else:
        # make api call because not found in cache
        response = requests.get(url)

        if response.ok:
            response_json = json.loads(response.text)

            # update cache
            _cache.update_cache(url, response_json)

            return response_json
        else:
            response.raise_for_status()
