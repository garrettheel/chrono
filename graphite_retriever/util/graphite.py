import logging

logger = logging.getLogger(__name__)


def _parse_result_line(line):
    meta, data = line.split('|', 1)

    data = map(lambda x: None if x == 'None' else float(x), data.split(','))
    return data

def parse_graphite_response(keys, content):
    lines = content.strip().split('\n')
    if len(keys) != len(lines):
        logger.error("Received invalid data from Graphite - expected {} lines but got {}"\
                     .format(len(keys), len(lines)))
        return

    result = {}
    for i, line in enumerate(lines):
        result[keys[i]] = _parse_result_line(line)
    return result
