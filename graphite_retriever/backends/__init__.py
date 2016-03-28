from .graphite import GraphiteBackend
from graphite_retriever.config import config


BACKENDS = {
    'graphite': GraphiteBackend
}


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
    backend_clazz = BACKENDS.get(kwargs.get('type'))
    return backend_clazz(**kwargs)
