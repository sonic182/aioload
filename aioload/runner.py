import asyncio
import aiohttp.client_exceptions
import statistics
from datetime import datetime
from datetime import timedelta

import aiohttp
import pandas as pd
from aioload.plot import render_plot


class Runner:

    def __init__(self, logger, args, **kwargs):
        self.logger = logger
        self.args = args
        self.kwargs = kwargs

    @classmethod
    async def request(cls, session, sem, logger, url, method, params=None,
                      headers=None, body=None, json=None):
        """Do request and return statics."""
        async with sem:
            req_data = cls.prepare_request(
                url, method, params, headers, body, json)
            logger.debug('doing request')

            before = datetime.now()
            try:
                # req_data options
                # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request  # noqa
                async with session.request(**req_data) as resp:
                    after = datetime.now()
                    # data = await resp.json()
                    res = {
                        'code': resp.status,
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
    def prepare_request(url, method, params, headers, body, json):
        """Prepare request."""
        req_data = {
            'url': url,
            'method': method
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

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=args.concurrency),
            timeout=aiohttp.ClientTimeout(
                sock_read=kwargs.pop('sock_read', 27),
                sock_connect=kwargs.pop('sock_connect', 3)
            )
        ) as session:
            target = kwargs.get('target', self.request)
            sem = asyncio.Semaphore(args.concurrency)
            # Send one request before test, for caching dns resolution
            # and keeping alive connection
            await target(session, sem, logger, **kwargs)

            statics = await asyncio.gather(*[
                target(session, sem, logger, **kwargs)
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
