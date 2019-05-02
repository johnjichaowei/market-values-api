import pytest
import logging
import os
from market_values_api.exceptions.market_value_client_error import MarketValueClientError

class MarketValueClient(object):

    def __init__(self, session):
        self.session = session

    async def get(self, company_symbol):
        async with self.session.get(f"{os.environ['MARKET_VALUE_HOST_URL']}/quote/{company_symbol}.AX") as response:
            if response.status != 200:
                raise MarketValueClientError(f"Failed to get market value for client, resposne code {response.status}")
            return await response.text()
