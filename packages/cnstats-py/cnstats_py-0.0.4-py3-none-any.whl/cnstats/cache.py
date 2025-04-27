import os
import pickle
import tempfile
import time
from typing import Optional


class _FileCache:
    def __init__(self, cache_dir: str) -> None:
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.cache")

    def set(self, key: str, value: str) -> None:
        cache_path = self._get_cache_path(key)
        with open(cache_path, "wb") as cache_file:
            pickle.dump(value, cache_file)

    def get(self, key: str) -> Optional[str]:
        cache_path = self._get_cache_path(key)

        # Guard clause: Check if cache file exists
        if not os.path.exists(cache_path):
            return None

        # Check the file's modification time
        mod_time = os.path.getmtime(cache_path)
        current_time = time.time()
        age_seconds = current_time - mod_time

        # Guard clause: Check if the cache is older than 7 days
        if age_seconds > 7 * 24 * 60 * 60:
            os.remove(cache_path)  # Remove the expired cache file
            return None  # Return None as the cache is expired

        # If cache exists and is not expired, load and return it
        with open(cache_path, "rb") as cache_file:
            return pickle.load(cache_file)

    def clear(self, key: str) -> None:
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)

    def clear_all(self) -> None:
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


# Create a default instance of FileCache
cache_dir = os.path.join(os.getenv("HOME", "out/cache"), ".cnstats_cache")
_default_cache = _FileCache(cache_dir)


def set(key: str, value: str) -> None:
    _default_cache.set(key, value)


def get(key: str) -> Optional[str]:
    return _default_cache.get(key)


# Add clear and clear_all functions for the default cache instance
def clear(key: str) -> None:
    _default_cache.clear(key)


def clear_all() -> None:
    _default_cache.clear_all()
