from universitybot.calls.cache import Cache
from datetime import timedelta
import unittest


class CacheTest(unittest.TestCase):
    def setUp(self):
        self.cache = Cache()
        self.delta_time = timedelta(hours=24)

    def test_get_cached(self):
        url1 = "https://www.google.com"
        response1 = "I'm a cache element!"
        response2 = "I'm a cache element2!"

        self.cache.update_cache(url1, response1)
        self.assertEqual(self.cache.get_cached(url1, self.delta_time), response1, "FAILURE")

        self.cache.update_cache(url1, response2)
        self.assertEqual(self.cache.get_cached(url1, self.delta_time), response2, "FAILURE")
