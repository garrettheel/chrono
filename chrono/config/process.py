import logging


__all__ = ['process_config']

logger = logging.getLogger(__name__)


def process_storage(config):
    from chrono.storage import get_storage_engine
    config['storage'] = get_storage_engine(config['storage'])


def process_backends(config):
    from chrono.backends import create_backend
    backends = []
    for c in config.get('backends', []):
        backend = create_backend(**c)
        backends.append(backend)
    config['backends'] = backends


def process_notifiers(config):
    from chrono.notifiers import type_to_notifier

    notifiers = []
    for c in config.get('notifiers', []):
        type_ = c.pop('type')
        notifier_cls = type_to_notifier(type_)
        notifiers.append(notifier_cls(**c))
    config['notifiers'] = notifiers


def process_watches(config):
    from chrono.watches import Watch
    from chrono.backends import get_backend

    watches = []
    for c in config.get('watches', []):
        c['backend'] = get_backend(config['backends'], c.get('backend', None))
        w = Watch(**c)
        watches.append(w)
    config['watches'] = watches


def process_config(config):
    process_storage(config)
    process_backends(config)
    process_notifiers(config)
    process_watches(config)
