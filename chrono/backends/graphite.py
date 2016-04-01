import logging
import requests

from . import Backend

logger = logging.getLogger(__name__)


def _parse_result_line(line):
    meta, data = line.split('|', 1)
    # TODO: may want alternate handling for None values
    data = [float(x) for x in data.split(',') if x != 'None']
    return data


def _parse_response(keys, content):
    lines = content.strip().split('\n')
    if len(keys) != len(lines):
        logger.error("Received invalid data from Graphite - expected {} lines but got {}"\
                     .format(len(keys), len(lines)))
        return

    result = {}
    for i, line in enumerate(lines):
        result[keys[i]] = _parse_result_line(line)
    return result


class GraphiteBackend(Backend):
    name = 'graphite'

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')

    def get_metrics(self, series):
        params = {
            'target': series.values(),
            'from': '-30minute',
            'until': 'now',
            'rawData': 'true',
        }

        try:
            resp = requests.get('{}/render'.format(self.url),
                                params=params,
                                timeout=5)
        except requests.Timeout:
            logger.error('Request to {} timed out.'.format(self.url))
            return None

        logger.debug("Fetching data from {}".format(resp.request.url))

        if resp.status_code != 200:
            logger.error("Error retrieving data from Graphite - {}".format(resp.status_code))
            return None

        return _parse_response(series.keys(), resp.content)
