import asynctest
import pytest
from aiohttp import web
from decimal import Decimal
from multidict import MultiDict, MultiDictProxy
from market_values_api.handlers import MarketValuesHandler

class TestMarketValuesHandler(object):

    @pytest.fixture
    def app(self, session):
        app = web.Application()
        app['client_session'] = session
        return app

    @pytest.fixture
    def request_class(self):
        with asynctest.patch('aiohttp.web.Request', autospec=True, scope=asynctest.LIMITED) as request_class:
            yield request_class

    @pytest.fixture
    def mock_request(self, app, request_class):
        def _mock_request_func(query_params={'companies': 'REA,CBA'}):
                request = request_class.return_value
                request.app = app
                request.query = MultiDictProxy(MultiDict(query_params))
                return request

        return _mock_request_func

    @pytest.fixture
    def service_class(self):
        with asynctest.patch(
            'market_values_api.services.MarketValuesService', autospec=True, scope=asynctest.LIMITED
        ) as service_class:
            yield service_class

    @pytest.fixture
    def mock_service(self, service_class):
        def _mock_service_func(market_values={'CBA': Decimal('123'), 'REA': Decimal('111')}):
            service = service_class.return_value
            service.get.return_value = market_values
            return service

        return _mock_service_func

    async def test_get_instantiates_market_values_service(self, mock_request, service_class):
        request = mock_request()
        await MarketValuesHandler().get(request)
        service_class.assert_called_once_with(request.app['client_session'])

    async def test_get_calls_market_values_service(self, mock_request, mock_service):
        request = mock_request({'companies': 'REA,CBA,ANZ'})
        service = mock_service()
        await MarketValuesHandler().get(request)
        service.get.assert_called_once_with(['REA', 'CBA', 'ANZ'])


    async def test_get_returns_market_values_as_json(self, mock_request, mock_service):
        market_values = {'CBA': Decimal('123.1245'), 'ANZ': Decimal('321.1122'), 'REA': Decimal('789.7878')}
        request = mock_request()
        service = mock_service(market_values)
        response = await MarketValuesHandler().get(request)
        assert 'application/json' in response.headers['Content-Type']
        assert response.text == '{"CBA": 123.1245, "ANZ": 321.1122, "REA": 789.7878}'

    @pytest.mark.usefixtures("mock_service")
    async def test_get_returns_400_if_companies_param_is_not_present(self, mock_request):
        request = mock_request({})
        with pytest.raises(web.HTTPBadRequest) as err:
            await MarketValuesHandler().get(request)
        assert 'The companies param is required' in str(err)
