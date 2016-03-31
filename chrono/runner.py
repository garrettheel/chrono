import logging

from .scheduler import Scheduler
from .storage import get_storage_engine


logger = logging.getLogger(__name__)


class Runner(object):

    def __init__(self, config):
        self.config = config
        self.scheduler = Scheduler()
        self.storage = get_storage_engine(config['storage'])

    def run(self):
        for watch in self.config['watches']:
            self.scheduler.add(30, self.handle_watch, watch)
        self.scheduler.run()

    def handle_watch(self, watch):
        watch_key = 'watch.{}'.format(watch.name)

        old_state = self.storage.get(watch_key)
        new_state, triggered = watch.check()

        if old_state != new_state:
            logger.info("State changed: {} => {}".format(old_state, new_state))

        self.storage.set(watch_key, new_state)
