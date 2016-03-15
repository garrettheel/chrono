import logging

import requests

from graphite_retriever.config import config
from graphite_retriever.util.graphite import parse_graphite_response

from .triggers import build_trigger

logger = logging.getLogger(__name__)


class Watch(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.series = kwargs.get('series', [])
        self.triggers = kwargs.get('triggers', [])

    def check(self):
        logger.info('Running check for {}'.format(self.name))
        server_url = config['server']['url']

        # TODO: ensure order of keys() and values() is consistent
        params = {
            'target': self.series.values(),
            'from': '-30minute',
            'until': 'now',
            'rawData': "true",
        }

        resp = requests.get('{}/render'.format(server_url), params=params)
        logger.info("Fetching data from {}".format(resp.request.url))

        if resp.status_code != 200:
            logger.error("Error retrieving data from Graphite - {}".format(resp.status_code))
            return

        result = parse_graphite_response(self.series.keys(), resp.content)

        print result

        # want to end up with
        {
            't': [None, None, None, 3.1, 2.1, 5.4]
        }
