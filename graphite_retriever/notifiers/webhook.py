import requests
import logging

from graphite_retriever.notifiers import Notifier


logger = logging.getLogger(__name__)


class WebhookNotifier(Notifier):
    name = 'webhook'

    def __init__(self, params):
        pass

    def notify(self):
        data = {

        }
        requests.get("", data=data)
