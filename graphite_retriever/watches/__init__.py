import logging

from graphite_retriever import graphite
from .triggers import build_trigger

logger = logging.getLogger(__name__)


class Watch(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.series = kwargs.get('series', [])
        self.triggers = kwargs.get('triggers', [])

    def check(self):
        logger.info('Running check for {}'.format(self.name))

        results = graphite.get_metrics(self.series)
        print results

        if not results:
            pass  # something went wrong
