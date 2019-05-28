"""Main module."""

import asyncio
import aiohttp
import statistics
from datetime import datetime
from datetime import timedelta
from argparse import ArgumentParser
from configparser import ConfigParser

from load_test.utils import get_logger
from load_test.plot import render_plot


async def request(session, sem, logger, config):
    """Do request and return statics."""
    async with sem:
        logger.debug('doing request')
        req_data = {
            'method': config['test']['method'],
            'url': config['test']['url']
        }

        if 'params' in config:
            req_data['params'] = dict(config['params'])

        if 'headers' in config:
            req_data['headers'] = dict(config['headers'])

        if 'body' in config['test']:
            req_data['data'] = config['test']['body']

        before = datetime.now()
        async with session.request(**req_data) as resp:
            after = datetime.now()
            # data = await resp.json()
            res = {
                'code': resp.status,
                'when': after,
                'duration': (after - before) / timedelta(milliseconds=1)
            }
            logger.debug('done request', extra=res)
            return res


async def start(logger, args, config):
    """Start script."""
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=args.concurrency),
        timeout=aiohttp.ClientTimeout(
            sock_read=config['http'].getint('sock_read', 30),
            sock_connect=config['http'].getint('sock_connect', 3),
        )
    ) as session:
        sem = asyncio.Semaphore(args.concurrency)
        statics = await asyncio.gather(*[
            request(session, sem, logger, config)
            for _ in range(args.number_of_requests)]
        )
        durations = []
        codes = {}
        for x in statics:
            codes[x['code']] = code = codes.get(x['code'], 0)
            codes[x['code']] = code + 1
            durations.append(x['duration'])

        logger.info('done', extra={
            'min': min(durations),
            'max': max(durations),
            'mean': statistics.mean(durations),
            'stdev': statistics.stdev(durations),
            'codes': codes,
            'concurrency': args.concurrency,
            'requests': args.number_of_requests,
        })
        if args.plot:
            render_plot(statics)


def get_arguments():
    """Get arguments."""
    parser = ArgumentParser()
    parser.add_argument('-s', '--settings', default='./config.ini')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-n', '--number_of_requests', type=int, default=100)
    parser.add_argument('-c', '--concurrency', type=int, default=10)
    parser.add_argument('--plot', action='store_true')
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
