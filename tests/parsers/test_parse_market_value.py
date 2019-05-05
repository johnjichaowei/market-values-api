import pytest
from decimal import Decimal
from market_values_api.parsers import ParseMarketValue
from market_values_api.exceptions import ParseMarketValueError

class TestParseMarketValue(object):

    def test_call_parses_market_value_in_billions(self, make_raw_response_text):
        market_value = ParseMarketValue(make_raw_response_text('74.305B')).call()
        assert market_value == Decimal('74305000000')

    def test_call_parses_market_value_in_millions(self, make_raw_response_text):
        market_value = ParseMarketValue(make_raw_response_text('12M')).call()
        assert market_value == Decimal('12000000')

    def test_call_parses_market_value_in_thousands(self, make_raw_response_text):
        market_value = ParseMarketValue(make_raw_response_text('.3051k')).call()
        assert market_value == Decimal('305.1')

    def test_call_parses_market_value_in_dollars(self, make_raw_response_text):
        market_value = ParseMarketValue(make_raw_response_text('123.56')).call()
        assert market_value == Decimal('123.56')

    def test_call_raise_exception_when_market_value_text_is_invalid(self, make_raw_response_text):
        with pytest.raises(ParseMarketValueError) as err:
            ParseMarketValue(make_raw_response_text('bla.122text')).call()
        assert "Failed to parse market value" in str(err)
