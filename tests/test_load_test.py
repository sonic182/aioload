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
async def test_request():
    """Test request function."""
    session = MagicMock()
    session.request.return_value = SessionRequestMock()
    session.request.return_value.status = 200
    sem = asyncio.Semaphore()
    logger = MagicMock()
    config = MagicMock()
    res = await request(session, sem, logger, config)

    assert res['code'] == 200
    assert isinstance(res['duration'], float)
