"""Test load_test.__init__.py file."""

import pytest
import asyncio
from unittest.mock import MagicMock
from load_test import request


class SessionRequestMock(MagicMock):
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
    session.request.return_value = SessionRequestMock()
    session.request.return_value.status = 200
    sem = asyncio.Semaphore()
    logger = MagicMock()
    url = MagicMock()
    method = MagicMock()
    res = await request(session, sem, logger, url, method)

    assert res['code'] == 200
    assert isinstance(res['duration'], float)
