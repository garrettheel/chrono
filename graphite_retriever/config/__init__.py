from graphite_retriever.config.read import read_config
from graphite_retriever.config.process import process_config


def get_config(path):
    config = read_config(path)
    if not config:
        return None
    process_config(config)
    return config
