import pytest
from decimal import Decimal
from market_values_api.parsers import ParseMarketValue
from market_values_api.exceptions import ParseMarketValueError

class TestParseMarketValue(object):

    @pytest.fixture
    def make_raw_text(self):
        def _make_raw_text_func(market_value_text):
            return ("<tr class=\"Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) \" data-reactid=\"51\">"
                        "<td class=\"C(black) W(51%)\" data-reactid=\"52\"><span data-reactid=\"53\">Market cap</span></td>"
                        "<td class=\"Ta(end) Fw(600) Lh(14px)\" data-test=\"MARKET_CAP-value\" data-reactid=\"54\">"
                            f"<span class=\"Trsdu(0.3s) \" data-reactid=\"55\">{market_value_text}</span>"
                        "</td>"
                    "</tr>")

        return _make_raw_text_func

    def test_call_parses_market_value_in_billions(self, make_raw_text):
        market_value = ParseMarketValue(make_raw_text('74.305B')).call()
        assert market_value == Decimal('74305000000')

    def test_call_parses_market_value_in_millions(self, make_raw_text):
        market_value = ParseMarketValue(make_raw_text('12M')).call()
        assert market_value == Decimal('12000000')

    def test_call_parses_market_value_in_thousands(self, make_raw_text):
        market_value = ParseMarketValue(make_raw_text('.3051k')).call()
        assert market_value == Decimal('305.1')

    def test_call_parses_market_value_in_dollars(self, make_raw_text):
        market_value = ParseMarketValue(make_raw_text('123.56')).call()
        assert market_value == Decimal('123.56')

    def test_call_raise_exception_when_market_value_text_is_invalid(self, make_raw_text):
        with pytest.raises(ParseMarketValueError) as err:
            ParseMarketValue(make_raw_text('bla.122text')).call()
        assert "Failed to parse market value" in str(err)
