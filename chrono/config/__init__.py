from chrono.config.read import read_config
from chrono.config.process import process_config


config = {}

def init_config(path):
    global config
    config.update(read_config(path))
    if config:
        process_config(config)
