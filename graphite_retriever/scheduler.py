import gevent
from gevent.pool import Pool


class Scheduler(object):

    def __init__(self, *watches):
        self.pool = Pool()
        self.active_watches = {}  # TODO: use for managing adding/removing
        for watch in watches:
            self.add(watch)

    def add(self, watch):
        self._schedule(30, watch.check)

    def _schedule(self, delay_seconds, func, *args, **kwargs):
        # TODO: some kind of check that we're still going
        self.pool.spawn(func, *args, **kwargs)

        g = gevent.Greenlet(self._schedule, delay_seconds, func, *args, **kwargs)
        self.pool.add(g)
        g.start_later(delay_seconds)

    def run(self):
        self.pool.join()
