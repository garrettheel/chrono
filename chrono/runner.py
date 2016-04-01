import logging

from .scheduler import Scheduler
from .watches.level import Level

logger = logging.getLogger(__name__)


class Runner(object):

    def __init__(self, config):
        self.config = config
        self.scheduler = Scheduler()
        self.storage = config['storage']

    def run(self):
        for watch in self.config['watches']:
            self.scheduler.add(30, self.handle_watch, watch)
        self.scheduler.run()

    def handle_watch(self, watch):
        watch_key = '.'.join(['watch', watch.name])

        old_state = self.storage.get(watch_key) or Level.UNKNOWN
        new_state, triggered = watch.check()

        logger.debug("{} triggers fired: {}".format(len(triggered),
            ', '.join(map(repr, triggered))))

        if old_state != new_state:
            if old_state == Level.UNKNOWN and new_state == Level.NORMAL:
                pass
            else:
                logger.info("State changed: {} => {}".format(old_state, new_state))
                self.notify(watch,
                            state=new_state, prev_state=old_state,
                            triggered=triggered)

        self.storage.set(watch_key, new_state)

    def notify(self, watch, state=None, prev_state=None, triggered=None):
        notify_ctx = {
            'watch': watch,
            'triggered': triggered,
            'prev_state': prev_state,
            'state': state
        }

        for notifier in self.config['notifiers']:
            notifier.notify(watch, notify_ctx)
