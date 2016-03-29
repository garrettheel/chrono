import logging
import six
from collections import defaultdict

from chrono.backends import get_backend
from .triggers import build_trigger
from .level import Level

logger = logging.getLogger(__name__)


class Watch(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.backend = kwargs.get('backend', None)
        self.series = kwargs.get('series', [])
        self.triggers = {}

        for raw_level, raw_triggers in kwargs.get('triggers', {}).iteritems():
            if isinstance(raw_triggers, six.string_types):  # shortcut for 1 item
                raw_triggers = [raw_triggers]
            level = Level.from_string(raw_level)
            self.triggers[level] = [build_trigger(t) for t in raw_triggers]

        self.state = Level.NORMAL  # TODO: may want to start at a "nil" state of sorts

    def check(self):
        logger.info('Running check for {}'.format(self.name))

        metrics = self.backend.get_metrics(self.series)
        if not metrics:
            return

        highest_level = Level.NORMAL
        triggered = []
        for level, triggers in self.triggers.iteritems():
            for trigger in triggers:
                logger.debug('Evaluating trigger: {}\nInput: {}'
                             .format(trigger, metrics))
                did_trigger = trigger.evaluate(metrics)
                logger.debug('Result for "{}" was {}'.format(trigger, did_trigger))

                if did_trigger:
                    triggered.append(trigger)
                    highest_level = max(level, highest_level)

        original_state = self.state
        self.state = highest_level
        return original_state, self.state, triggered
