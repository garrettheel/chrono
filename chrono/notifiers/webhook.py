import requests
import logging

from . import Notifier


logger = logging.getLogger(__name__)


class WebhookNotifier(Notifier):
    name = 'webhook'

    def __init__(self, **params):
        self.url = params.get('url')

    def notify(self, ctx):
        data = {

        }
        requests.get(self.url, data=data)
