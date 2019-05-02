import asynctest
import pytest

@pytest.fixture
def session():
    with asynctest.patch('aiohttp.ClientSession', autospec=True, scope=asynctest.LIMITED) as session_class:
        yield session_class.return_value
