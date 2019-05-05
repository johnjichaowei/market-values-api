import asynctest
import pytest
import os

@pytest.fixture
def host_url():
    return 'http://dummy-url'

@pytest.fixture
def set_url_env(host_url):
    with asynctest.patch.dict(os.environ, {'MARKET_VALUE_HOST_URL': host_url}, scope=asynctest.LIMITED) as patched_env:
        yield patched_env

@pytest.fixture
def session(set_url_env):
    with asynctest.patch('aiohttp.ClientSession', autospec=True, scope=asynctest.LIMITED) as session_class:
        yield session_class.return_value

@pytest.fixture
def response_class():
    with asynctest.patch('aiohttp.ClientResponse', autospec=True, scope=asynctest.LIMITED) as response_class:
        yield response_class

@pytest.fixture
def mock_response(session, response_class):
    def _mock_response_func(response_code=200, response_text='OK'):
            response = response_class.return_value
            response.status = response_code
            response.text = asynctest.CoroutineMock(return_value=response_text)
            response.__aenter__.return_value = response
            session.get.return_value = response

    return _mock_response_func

@pytest.fixture
def make_raw_response_text():
    def _make_raw_response_text_func(market_value_text):
        return ("<tr class=\"Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) \" data-reactid=\"51\">"
                    "<td class=\"C(black) W(51%)\" data-reactid=\"52\"><span data-reactid=\"53\">Market cap</span></td>"
                    "<td class=\"Ta(end) Fw(600) Lh(14px)\" data-test=\"MARKET_CAP-value\" data-reactid=\"54\">"
                        f"<span class=\"Trsdu(0.3s) \" data-reactid=\"55\">{market_value_text}</span>"
                    "</td>"
                "</tr>")

    return _make_raw_response_text_func
