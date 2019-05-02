import re
from decimal import Decimal
from market_values_api.exceptions.parse_market_value_error import ParseMarketValueError

class ParseMarketValue(object):

    def __init__(self, raw_text):
        self.raw_text = raw_text

    def call(self):
        return self._parse_market_value()

    def _parse_market_value(self):
        p = re.compile(
            r'<td.+?data-test="MARKET_CAP-value".*?><span.*?>\s*(?P<value>\d*\.?\d*)(?P<unit>[BbMmKk]?)\s*</span></td>'
        )
        match = p.search(self.raw_text)
        if match != None:
            return self._convert_value(match.group('value'), match.group('unit'))
        raise ParseMarketValueError('Failed to parse market value')

    def _convert_value(self, value, unit):
        multiplier = {
            'B': 1000000000,
            'M': 1000000,
            'K': 1000,
            '':  1
        }[unit.upper()]

        return Decimal(value) * multiplier
