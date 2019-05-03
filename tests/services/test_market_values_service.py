import asynctest
import pytest
from decimal import Decimal
from market_values_api.services import MarketValuesService

class TestMarketValuesService(object):

    @pytest.fixture
    def company_list(self):
        return ['CBA', 'ANZ', 'REA']

    @pytest.fixture
    def market_values(self):
        return {'CBA': Decimal('123'), 'ANZ': Decimal('321'), 'REA': Decimal('789')}

    @pytest.fixture
    def repository_class(self):
        with asynctest.patch(
            'market_values_api.repositories.MarketValueRepository',
            autospec=True, scope=asynctest.LIMITED
        ) as repository_class:
            yield repository_class

    @pytest.fixture
    def repository(self, repository_class, market_values):
        def _side_effect(company):
            if market_values.get(company) == None:
                raise Exception('Unexpected error')
            return (company, market_values[company])

        repository = repository_class.return_value
        repository.get.side_effect = _side_effect
        return repository

    @pytest.mark.usefixtures("repository")
    async def test_get_instantiate_one_market_value_repository(self, session, company_list, repository_class):
        await MarketValuesService(session).get(company_list)
        repository_class.assert_called_once_with(session)

    async def test_get_calls_market_value_repository_for_each_company(self, session, company_list, repository):
        await MarketValuesService(session).get(company_list)
        assert repository.get.call_count == 3

    @pytest.mark.usefixtures("repository")
    async def test_get_returns_market_values_as_a_dict(self, session, company_list, market_values):
        result = await MarketValuesService(session).get(company_list)
        assert result == market_values

    @pytest.mark.usefixtures("repository")
    async def test_get_reraises_exception_occurred_in_async_task(self, session, company_list):
        with pytest.raises(Exception) as err:
            await MarketValuesService(session).get(company_list + ['CompanyNotExist'])
        assert 'Unexpected error' in str(err)
