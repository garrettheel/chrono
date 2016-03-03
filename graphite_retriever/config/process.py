import logging

__all__ = ['process_config']

logger = logging.getLogger(__name__)


def process_notifiers(config):
    from graphite_retriever.notifiers import type_to_notifier

    notifiers = []
    for c in config.get('notifiers', []):
        type_ = c.pop('type')
        notifier_cls = type_to_notifier(type_)
        notifiers.append(notifier_cls(c))
    config['notifiers'] = notifiers


def process_watches(config):
    from graphite_retriever.watches import Watch

    watches = []
    for c in config.get('watches', []):
        w = Watch(**c)
        watches.append(w)
    config['watches'] = watches


def process_config(config):
    process_notifiers(config)
    process_watches(config)
