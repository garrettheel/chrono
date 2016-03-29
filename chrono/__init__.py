import sys
import argparse
import logging

from .runner import Runner
from .scheduler import Scheduler


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Watches the result of graphite queries')
    parser.add_argument('-c', '--config',
                        help='path to a configuration file. defaults to config.py in cwd', default='config.json')
    parser.add_argument('--log-level',
                        help="log level", default='DEBUG',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'])
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level),
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)

    logger.info("Starting chrono")

    from chrono.config import init_config, config
    init_config(args.config)
    if not config:
        sys.exit(1)

    runner = Runner(config)
    runner.run()

if __name__ == '__main__':
    main()
