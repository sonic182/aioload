"""Runner module."""
import asyncio
import statistics
from datetime import datetime
from datetime import timedelta

import pandas as pd
from aioload.plot import render_plot
import aiosonic
from aiosonic.timeout import Timeouts
from aiosonic.connectors import TCPConnector


class Runner:
    """Runner class."""

    def __init__(self, logger, args, **kwargs):
        """Initialize runner."""
        self.logger = logger
        self.args = args
        self.kwargs = kwargs
        self.connector = TCPConnector(pool_size=args.concurrency)

        logger.info('preparing_requests')
        self.requests_data = [
            self.prepare_request(**kwargs)
            for _ in range(args.number_of_requests)
        ]
        logger.info('prepared_requests')

    async def request(self, sem, logger, req_data):
        """Do request and return statics."""
        async with sem:
            logger.debug('doing request')

            before = datetime.now()
            try:
                # req_data options
                resp = await aiosonic.request(
                    **req_data, connector=self.connector)
                after = datetime.now()
                res = {
                    'code': resp.status_code,
                    'when': after,
                    'duration': (after - before) / timedelta(
                        milliseconds=1)
                }
                logger.debug('done request', extra=res)
                return res
            except Exception:
                after = datetime.now()
                logger.exception('some_exception')
                return {
                    'code': 'X',
                    'when': before,
                    'duration': (after - before) / timedelta(milliseconds=1)
                }

    @staticmethod
    def prepare_request(url, method, params=None, headers=None, body=None,
                        json=None, **kwargs):
        """Prepare request."""
        req_data = {
            'url': url,
            'method': method,
            'timeouts': Timeouts(
                sock_read=kwargs.get('sock_read', 30),
                sock_connect=kwargs.get('sock_connect', 30),
            )
        }

        if params:
            req_data['params'] = dict(params)

        if headers:
            req_data['headers'] = dict(headers)

        if body:
            req_data['data'] = body

        if json:
            req_data['json'] = json
        return req_data

    async def start(self):
        """Start script."""
        logger = self.logger
        args = self.args
        kwargs = self.kwargs

        target = kwargs.get('target', self.request)
        sem = asyncio.Semaphore(args.concurrency)

        logger.info('starting_requests')
        statics = await asyncio.gather(*[
            target(sem, logger, req_data)
            for req_data in self.requests_data
        ])

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
            index=when
        )

        # logger result
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
