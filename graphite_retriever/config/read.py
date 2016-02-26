import os
import json
import logging

import jsonschema

logger = logging.getLogger(__name__)

def read_config(conf_path):
    config = None
    try:
        with open(conf_path, 'r') as f:
            config = json.load(f)
            jsonschema.validate(config, _load_schema())
    except IOError as e:
        logger.error("Unable to read config file '{}'".format(conf_path))
    except ValueError as e:
        logger.error("Unable to parse config file '{}': {}".format(
            conf_path, e.message
        ))
    except jsonschema.ValidationError as e:
        config = None
        logger.error("Config file failed schema validation:\n{}".format(
            e.message
        ))
    return config


def _load_schema():
    config_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(config_dir, 'schema.json')
    with open(schema_file, "r") as schema_f:
        schema = json.load(schema_f)
    return schema
