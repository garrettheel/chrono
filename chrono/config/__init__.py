from chrono.config.read import read_config
from chrono.config.process import process_config


config = {}

def init_config(path):
    global config
    new_config = read_config(path)
    if new_config:
        config.update(new_config)
        process_config(config)
