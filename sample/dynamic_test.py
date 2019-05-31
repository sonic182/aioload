

import asyncio
import random
from configparser import ConfigParser

from load_test.utils import get_logger

from load_test import start
from load_test import request
from load_test import get_arguments

PARAMS = [{
    'query': 'something',
}, {
    'query': 'red',
}, {
    'query': 'green',
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
    config.read(args.settings)
    logger, uuid = get_logger(args, config)
    logger.info('Starting script...')
    loop = asyncio.get_event_loop()

    kwargs = {
        'url': 'http://localhost:8000/search',
        'method': 'get',
        'params': dict(config['params']),
        'target': my_request
    }
    loop.run_until_complete(start(logger, args, **kwargs))
    logger.info('Exiting script...')


if __name__ == '__main__':
    main()
