import memcache

cache = memcache.Client(['127.0.0.1:11211'], debug=True)

def set(key, value, timeout=60):
    return cache.set(key=key, val=value, time=timeout)


def get(key):
    return cache.get(key=key)


def delete(key):
    return cache.delete(key)
