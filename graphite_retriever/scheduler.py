import logging
import gevent
import signal

from gevent.pool import Pool


logger = logging.getLogger(__name__)

SIGNALS_TO_NAMES = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )


class Scheduler(object):

    def __init__(self, *watches):
        self.scheduled_pool = Pool()
        self.active_pool = Pool()

        self.shutting_down = False
        self.stop_event = gevent.event.Event()

        self.active_watches = {}  # TODO: use for managing adding/removing
        for watch in watches:
            self.add(watch)

    def add(self, watch):
        self._schedule(30, watch.check)

    def _schedule(self, delay_seconds, func, *args, **kwargs):
        if self.shutting_down:
            return

        self.active_pool.spawn(func, *args, **kwargs)

        g = gevent.Greenlet(self._schedule, delay_seconds, func, *args, **kwargs)
        self.scheduled_pool.add(g)
        g.start_later(delay_seconds)

    def handle_signal(self, signal, frame):
        logger.info('Received {}. Shutting down.'.format(SIGNALS_TO_NAMES.get(signal)))
        self.shutting_down = True
        self.stop_event.set()

    def run(self):
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, self.handle_signal)
        self.stop_event.wait()
        # TODO: could give running greenlets a chance to finish
