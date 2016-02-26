import gevent


class Scheduler(object):
    
    def __init__(self):
        pass


def schedule(delay_seconds, func, *args, **kwargs):
    # some kind of check that we're still going
    gevent.spawn_later(0, func, *args, **kwargs)
    gevent.spawn_later(delay_seconds, schedule, delay_seconds, func, *args, **kwargs)
