"""Test load_test.__init__.py file."""

import pytest
import asyncio
import random
from datetime import datetime
from unittest.mock import MagicMock
from aioload import request
from aioload import start
from aioload import get_arguments


class AsyncMagicMock(MagicMock):
    """Mock for Session Request."""

    async def __aenter__(self):
        """Mock aenter."""
        return self

    async def __aexit__(self, *args, **kwargs):
        """Mock aexit."""
        return MagicMock()


@pytest.mark.asyncio
async def test_request(config):
    """Test request function."""
    session = MagicMock()
    session.request.return_value = AsyncMagicMock()
    session.request.return_value.status = 200
    sem = asyncio.Semaphore()
    logger = MagicMock()
    url = 'http://someurl:8080'
    method = 'get'
    params = {
        'foo': 'bar'
    }
    headers = {
        'accept-encoding': 'gzip,deflate'
    }
    body = 'somebody'
    json = {'foo': 'bar'}
    res = await request(
        session, sem, logger, url, method, params, headers, body, json)

    assert res['code'] == 200
    assert isinstance(res['duration'], float)


@pytest.mark.asyncio
async def test_request_raise_exception(config):
    """Test request function."""
    session = MagicMock()
    session.request.side_efect = Exception('some exception')
    sem = AsyncMagicMock()
    logger = MagicMock()
    url = 'http://someurl:8080'
    method = 'get'
    res = await request(
        session, sem, logger, url, method)

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
async def test_start(config, mocker):
    """Test request function."""
    mocker.patch('aioload.request', new=mock_request)
    mocker.patch('aioload.render_plot')
    session = MagicMock()
    session.request.side_efect = Exception('some exception')
    logger = MagicMock()
    args = MagicMock()
    args.concurrency = 1
    args.number_of_requests = 10
    args.plot = True
    assert await start(logger, args) is None


@pytest.mark.asyncio
async def test_get_argument(config, mocker):
    """Test request function."""
    mocker.patch('argparse.ArgumentParser.parse_args')
    assert get_arguments()
