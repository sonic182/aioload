"""Test load_test.__init__.py file."""

import asyncio
import random
from datetime import datetime
from datetime import timedelta
from argparse import Namespace
from unittest.mock import MagicMock
from configparser import ConfigParser

import pandas as pd
import pytest

from aioload.runner import Runner
from aioload import get_arguments
from aioload.plot import render_plot
from aioload_utils import get_logger


class AsyncMagicMock(MagicMock):
    """Mock for Session Request."""

    async def __aenter__(self):
        """Mock aenter."""
        return self

    async def __aexit__(self, *args, **kwargs):
        """Mock aexit."""
        return MagicMock()


@pytest.mark.asyncio
async def test_request(mocker):
    """Test request function."""
    response = MagicMock()
    response.status_code = 200

    async def return_resp(*args, **kwargs):
        return response
    resp = mocker.patch(
        'aioload.runner.aiosonic.HTTPClient.request',
        return_value=return_resp())
    mocker.patch('aioload.runner.Runner.prepare_request')
    resp.status_code = 200
    sem = asyncio.Semaphore()
    logger = MagicMock()
    args = MagicMock(
        number_of_requests=1, concurrency=1, insecure=False)
    runner = Runner(MagicMock(), args)
    res = await runner.request(
        sem, logger, {})

    assert res['code'] == 200
    assert isinstance(res['duration'], float)


@pytest.mark.asyncio
async def test_request_raise_exception():
    """Test request function."""
    session = MagicMock()
    session.request.side_efect = Exception('some exception')
    sem = AsyncMagicMock()
    logger = MagicMock()
    res = await Runner.request(
        session, sem, logger, {})

    assert res['code'] == 'X'
    assert isinstance(res['duration'], float)


DURATIONS = range(1, 100)


async def mock_request(*args, **kwargs):
    """Mocked request method."""
    return {
        'code': 200,
        'when': datetime.now(),
        'duration': random.choice(DURATIONS)
    }


@pytest.mark.asyncio
async def test_start(mocker):
    """Test request function."""
    mocker.patch('aioload.runner.Runner.request', new=mock_request)
    mocker.patch('aioload.runner.render_plot')
    session = MagicMock()
    session.request.side_efect = Exception('some exception')
    logger = MagicMock()
    args = MagicMock()
    args.concurrency = 1
    args.number_of_requests = 10
    args.plot = True
    kwargs = {
        'url': 'foo',
        'method': 'get'
    }
    assert await Runner(logger, args, **kwargs).start() is None


@pytest.mark.asyncio
async def test_get_argument(mocker):
    """Test request function."""
    mocker.patch('argparse.ArgumentParser.parse_args')
    assert get_arguments()


@pytest.mark.asyncio
async def test_do_load_test_sample_server(app, aiohttp_server):
    """Do load test to sample server."""
    server = await aiohttp_server(app)
    kwargs = {
        'url': 'http://localhost:{}'.format(server.port),
        'method': 'post',
        'params': {'foo': 'bar'},
        'headers': {'foo': 'bar'},
        'json': {'foo': 'bar'},
        'body': 'foo',
    }
    config = ConfigParser()
    config.add_section('logging')
    args = Namespace(
        debug=False,
        verbose=True,
        number_of_requests=100,
        plot=False,
        concurrency=10,
        insecure=False
    )
    logger, _uuid = get_logger(args, config)
    await Runner(logger, args, **kwargs).start()
    await server.close()


@pytest.mark.asyncio
async def test_render_plot(mocker):
    """Do load test to sample server."""
    mocker.patch('aioload.plot.plt')
    statics = [{
        'code': 200
    }, {
        'code': 200
    }]
    durations = [30, 35]
    when = [datetime.now() - timedelta(seconds=3), datetime.now()]
    durations_serie = pd.Series(
        durations,
        index=when
    )
    render_plot(statics, durations_serie)


def test_init(mocker):
    """Test init."""
    import aioload
    mocker.patch.object(aioload, "main", return_value=42)
    mocker.patch.object(aioload, "__name__", "__main__")
    aioload.init()


def test_uvloop_not_installed(mocker):
    """Test uvloop not in module."""
    uvloop = MagicMock()
    uvloop.install = MagicMock(side_effect=ImportError())
    try:
        mocker.patch('aioload.uvloop', new=uvloop)
        import sys
        sys.modules['uvloop'] = uvloop
        if 'aioload' in sys.modules:
            del sys.modules['aioload']
        import aioload
        assert aioload
    except AttributeError:
        # not uvloop for windows
        pass


def test_main(mocker):
    """Test uvloop not in module."""
    mocker.patch('aioload.ConfigParser')
    mocker.patch('aioload.get_arguments')
    mocker.patch('aioload.asyncio.get_event_loop')
    mocker.patch('aioload.Runner')
    mocker.patch('aioload.get_logger', return_value=(MagicMock(), MagicMock()))
    from aioload import main
    main()
