import asyncio
import market_values_api.repositories as repositories

class MarketValuesService(object):
    def __init__(self, session):
        self.session = session

    async def get(self, company_list):
        repo = repositories.MarketValueRepository(self.session)
        result = await asyncio.gather(*(repo.get(company) for company in company_list))
        return dict(result)
