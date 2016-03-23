import logging
import six
from collections import defaultdict

from graphite_retriever import graphite
from .triggers import build_trigger

logger = logging.getLogger(__name__)


class Watch(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.series = kwargs.get('series', [])
        self.triggers = {}

        for level, raw_triggers in kwargs.get('triggers', {}).iteritems():
            if isinstance(raw_triggers, six.string_types):  # shortcut for 1 item
                raw_triggers = [raw_triggers]
            self.triggers[level] = [build_trigger(t) for t in raw_triggers]

    def check(self):
        logger.info('Running check for {}'.format(self.name))

        metrics = graphite.get_metrics(self.series)  # todo: better var name
        if not metrics:
            return

        for level, triggers in self.triggers.iteritems():
            for trigger in triggers:
                logger.debug('Evaluating trigger: {}\nInput: {}'
                             .format(trigger, metrics))
                result = trigger.evaluate(metrics)
                logger.debug('Result for "{}" was {}'.format(trigger, result))
