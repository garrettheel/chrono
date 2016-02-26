import logging
from six import with_metaclass

logger = logging.getLogger(__name__)
registry = {}


class NotifierMeta(type):
    def __new__(mcs, name, bases, params):
        clz = super(NotifierMeta, mcs).__new__(mcs, name, bases, params)
        if 'name' in params:
            registry[params['name']] = clz
            
        return clz

class Notifier(with_metaclass(NotifierMeta)):
    def __init__(self):
        pass
        
        
def type_to_notifier(type_):
    return registry.get(type_, None)


from webhook import WebhookNotifier
