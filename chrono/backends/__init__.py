from six import with_metaclass

from chrono.config import config


registry = {}


class BackendMeta(type):
    def __new__(mcs, name, bases, params):
        clz = super(BackendMeta, mcs).__new__(mcs, name, bases, params)
        if 'name' in params:
            registry[params['name']] = clz
        return clz


class Backend(with_metaclass(BackendMeta)):
    def to_json(self):
        return self.name


def get_backend(backends, name):
    if name is None:  # try and use a default
        if len(backends) != 1:
            raise ValueError("There should be exactly 1 backend to get a default, "+\
                             "instead got {}".format(len(backends)))
        return backends[0]
    try:
        return next(b for b in backends if b['name'] == name)
    except StopIteration:
        raise ValueError("Unknown backend: {}".format(backend))


def create_backend(**kwargs):
    backend_clazz = registry.get(kwargs.get('type'))
    return backend_clazz(**kwargs)


from .graphite import GraphiteBackend
