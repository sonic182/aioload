"""Main module."""

import asyncio
import aiohttp
from argparse import ArgumentParser
from configparser import ConfigParser

from load_test.utils import get_logger


async def request(session, url, config):
    """Do request and return statics."""


async def start(logger, args, config):
    """Start script."""
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=args.concurrency),
        timeout=aiohttp.ClientTimeout(
            sock_read=config['http'].getint('sock_read', 30),
            sock_connect=config['http'].getint('sock_connect', 3),
        )
    ) as session:
        pass


def get_arguments():
    """Get arguments."""
    parser = ArgumentParser()
    parser.add_argument('-s', '--settings', default='./config.ini')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-n', '--number_of_requests', type=int, default=100)
    parser.add_argument('-c', '--concurrency', type=int, default=10)
    return parser.parse_args()


def main():
    """Start script."""
    args = get_arguments()
    config = ConfigParser()
    config.add_section('logging')
    config.read(args.settings)
    logger, uuid = get_logger(args, config)
    logger.info('Starting script...')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(logger, args, config))
    logger.info('Exiting script...')


if __name__ == '__main__':
    main()
