

import asyncio
import random
from configparser import ConfigParser

from aioload.utils import get_logger

from aioload.runner import Runner
from aioload import get_arguments


PARAMS = [{
    'name': 'foo',
}, {
    'name': 'bar',
}, {
    'name': 'baz',
}]


class CustomRunner(Runner):

    async def request(self, *args, **kwargs):
        """Updates params in a random way."""
        kwargs['params'].update(random.choice(PARAMS))
        return await super(CustomRunner, self).request(*args, **kwargs)


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
    }
    loop.run_until_complete(Runner(logger, args, **kwargs).start())
    logger.info('Exiting script...')


if __name__ == '__main__':
    main()
