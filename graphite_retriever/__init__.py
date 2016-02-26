import sys
import argparse
import logging

logger = logging.getLogger(__name__)
    

def main():
    parser = argparse.ArgumentParser(description='Watches the result of graphite queries')
    parser.add_argument('-c', '--config',
                        help='path to a configuration file. defaults to config.py in cwd', default='config.json')
    parser.add_argument('--log-level',
                        help="log level", default='INFO',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'])
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level),
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    from graphite_retriever.config import get_config
    config = get_config(args.config)
    
    if not config:
        sys.exit(1)
        
    logger.info("Starting graphite-retriever")
    
    # start something
    



if __name__ == '__main__':
    main()
