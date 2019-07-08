

import random
from argparse import ArgumentParser
from aiohttp import web


STATUSES = [200, 202, 401, 500]


async def hello_handler(request):
    """Dummy handler."""
    return web.Response(
        text='Hello {}'.format(request.query.get('name', 'people')),
        status=random.choice(STATUSES)
    )


def get_app():
    """Get sample app."""
    app = web.Application()
    app.router.add_get('/hello', hello_handler)
    return app


def main():
    """Start sample app."""
    app = get_app()
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    web.run_app(app, port=args.port)


if __name__ == '__main__':
    main()
