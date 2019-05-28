
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def config():
    return {
        'test': {
            'method': 'get',
            'url': 'foo',
            'body': 'foo'
        },
        'params': [],
        'headers': []
    }
