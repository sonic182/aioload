"""Main module."""

import pandas as pd
import asyncio
import aiohttp
import aiohttp.client_exceptions
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
        try:
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
        except Exception:
            after = datetime.now()
            logger.exception('some_exception')
            return {
                'code': 'X',
                'when': after,
                'duration': (after - before) / timedelta(milliseconds=1)
            }


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
        # Send one request before test, for caching dns resolution
        # and keeping alive connection
        await request(session, sem, logger, config)

        statics = await asyncio.gather(*[
            request(session, sem, logger, config)
            for _ in range(args.number_of_requests)]
        )
        durations = []
        when = []
        codes = {}
        for x in statics:
            codes[x['code']] = code = codes.get(x['code'], 0)
            codes[x['code']] = code + 1
            durations.append(x['duration'])
            when.append(x['when'])

        serie = pd.Series(
            durations,
            index=pd.date_range(
                min(when),
                max(when),
                periods=len(durations),
            )
        )

        logger.info('done', extra={
            'min': '{}ms'.format(round(min(durations), 2)),
            'max': '{}ms'.format(round(max(durations), 2)),
            'mean': '{}ms'.format(round(serie.mean(), 2)),
            'req/s': serie.resample('1s').count().mean(),
            'req/q_std': round(serie.resample('1s').count().std(), 2),
            'stdev': round(statistics.stdev(durations), 2),
            'codes': codes,
            'concurrency': args.concurrency,
            'requests': args.number_of_requests,
        })
        if args.plot:
            render_plot(statics, serie)


def get_arguments():
    """Get arguments."""
    parser = ArgumentParser()
    parser.add_argument('-s', '--settings',
                        default='./config.ini', help='default: ./config.ini')
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
    config.read(args.settings)
    logger, uuid = get_logger(args, config)
    logger.info('Starting script...')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(logger, args, config))
    logger.info('Exiting script...')


if __name__ == '__main__':
    main()
