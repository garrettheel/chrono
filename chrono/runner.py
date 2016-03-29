import logging

from .scheduler import Scheduler


logger = logging.getLogger(__name__)


class Runner(object):

    def __init__(self, config):
        self.config = config
        self.scheduler = Scheduler()

    def run(self):
        for watch in self.config['watches']:
            self.scheduler.add(30, self.handle_watch, watch)
        self.scheduler.run()

    def handle_watch(self, watch):
        old_state, new_state, triggered = watch.check()

        if old_state != new_state:
            logger.info("State changed: {} => {}".format(old_state, new_state))
