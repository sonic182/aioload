

from aiohttp import web
import random


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
    web.run_app(app, port='8000')


if __name__ == '__main__':
    main()
