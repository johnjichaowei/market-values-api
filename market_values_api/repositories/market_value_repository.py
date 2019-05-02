import market_values_api.repositories.clients.market_value_client as client_module
import market_values_api.repositories.parsers.parse_market_value as parser_module

class MarketValueRepository(object):

    def __init__(self, session):
        self.session = session

    async def get(self, company_symbol):
        raw_text = await client_module.MarketValueClient(self.session).get(company_symbol)
        market_value = parser_module.ParseMarketValue(raw_text).call()
        return (company_symbol, market_value)
