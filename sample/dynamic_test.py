

import asyncio
import random
from configparser import ConfigParser

from aioload.utils import get_logger

from aioload import start
from aioload import request
from aioload import get_arguments

PARAMS = [{
    'name': 'foo',
}, {
    'name': 'bar',
}, {
    'name': 'baz',
}]


async def my_request(*args, **kwargs):
    """Updates params in a random way."""
    kwargs['params'].update(random.choice(PARAMS))
    return await request(*args, **kwargs)


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
        'url': 'http://localhost:8000',
        'method': 'get',
        'params': dict(config['params']),
        'target': my_request
    }
    loop.run_until_complete(start(logger, args, **kwargs))
    logger.info('Exiting script...')


if __name__ == '__main__':
    main()
