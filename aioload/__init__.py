"""Main module."""

import asyncio
from argparse import ArgumentParser
from configparser import ConfigParser

from aioload_utils import get_logger
from aioload.runner import Runner

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass


def get_arguments():
    """Get arguments."""
    parser = ArgumentParser()
    parser.add_argument('testfile', help='Test file to be executed')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='true if present')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help='true if present')
    parser.add_argument('-n', '--number_of_requests', type=int,
                        default=100, help='number of requests to be done, '
                        'default: 100')
    parser.add_argument('-c', '--concurrency', type=int, default=10,
                        help='concurrency (requests at the same time), '
                        'default: 10')
    parser.add_argument('--plot', action='store_true',
                        help="draw charts if present")
    return parser.parse_args()


def main():
    """Start script."""
    args = get_arguments()
    config = ConfigParser()
    config.add_section('logging')
    config.read(args.testfile)
    logger, uuid = get_logger(args, config)
    logger.info('Starting script...')
    loop = asyncio.get_event_loop()
    kwargs = {
        'url': config['test']['url'],
        'method': config['test']['method'],
        'params': dict(config['params']),
        'headers': dict(config['headers']),
        'sock_read': config['http'].getint('sock_read', 30),
        'sock_connect': config['http'].getint('sock_connect', 3),
    }
    runner = Runner(logger, args, **kwargs)
    loop.run_until_complete(runner.start())
    logger.info('Exiting script...')


def init():
    """Init function."""
    if __name__ == '__main__':
        main()


init()
