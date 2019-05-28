
import pytest


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
