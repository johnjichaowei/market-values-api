import market_values_api.clients as clients
import market_values_api.parsers as parsers
import logging

class MarketValueRepository(object):

    def __init__(self, session):
        self.session = session

    async def get(self, company_symbol):
        logging.info(f"Started retrieving market value for {company_symbol}")
        raw_text = await clients.MarketValueClient(self.session).get(company_symbol)

        logging.info(f"Started parsing market value for {company_symbol}")
        market_value = parsers.ParseMarketValue(raw_text).call()

        logging.info(f"Finished parsing market value for {company_symbol}, market value {market_value}")
        return (company_symbol, market_value)
