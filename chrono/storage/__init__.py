
def get_storage_engine(config):
    from .local import LocalBackedStorage
    return LocalBackedStorage()


class Storage(object):
    def __init__(self):
        pass

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def enqueue(self, check, *args, **kwargs):
        raise NotImplementedError
