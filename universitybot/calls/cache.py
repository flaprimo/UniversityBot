from datetime import datetime


class Cache:
    def __init__(self, cache_size=200):
        self.cache = []
        self.cache_size = cache_size

    def get_cached(self, url, time_delta):
        cached_element = list(filter(lambda x: x['url'] == url, self.cache))

        if len(cached_element) > 0 and datetime.now() - cached_element[0]['time'] < time_delta:
            return cached_element
        else:
            return None

    def update_cache(self, url, content):
        # remove outdated cache
        self.cache = list(filter(lambda x: x['url'] != url, self.cache))

        # pop oldest element from cache
        if len(self.cache) >= self.cache_size:
            self.cache.pop(0)

        # add new element to cache
        self.cache.append({
            'url': url,
            'content': content,
            'time': datetime.now()
        })
