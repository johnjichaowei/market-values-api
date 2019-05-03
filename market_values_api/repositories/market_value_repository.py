import market_values_api.clients as clients
import market_values_api.parsers as parsers

class MarketValueRepository(object):

    def __init__(self, session):
        self.session = session

    async def get(self, company_symbol):
        raw_text = await clients.MarketValueClient(self.session).get(company_symbol)
        market_value = parsers.ParseMarketValue(raw_text).call()
        return (company_symbol, market_value)
