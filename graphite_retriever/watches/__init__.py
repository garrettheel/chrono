import logging

from graphite_retriever.config import config
from .parser import build_trigger

logger = logging.getLogger(__name__)


class Watch(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.sources = kwargs.get('sources', [])
        self.triggers = kwargs.get('triggers', [])

    def check(self):
        logger.info('Running check for {}'.format(self.name))
        server_url = config['server']['url']

        import requests

        query = escape.url_escape(query)

        query_params = {
            'target': '',
            'from': '',
            'until': '',
            'raw_data': True
        }

        requests.get('{}/render/'.format())
