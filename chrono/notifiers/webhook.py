import json
import requests
import logging

from . import Notifier


logger = logging.getLogger(__name__)


def dumper(o):
    try:
        return o.to_json()
    except:
        return o.__dict__


class WebhookNotifier(Notifier):
    name = 'webhook'

    def __init__(self, **params):
        self.url = params.get('url')

    def notify(self, watch, ctx):
        data = json.dumps(ctx, default=dumper)
        requests.post(self.url,
                      headers={'content-type': 'application/json'},
                      data=data)
