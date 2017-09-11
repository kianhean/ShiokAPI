from promos import api as promo_api
from draws import api as draw_api

# Testing Promo APIs

def test_get_promos():
    result = promo_api.get_promos('https://www.couponese.com/store/uber.com/')
    assert isinstance(result, dict)


def test_promo_loop():
    result = promo_api.promo_loop('{"uber":"https://www.couponese.com/store/uber.com/"}')
    assert isinstance(result, str)
    assert len(result) > 20


def test_FourD():
    result = draw_api.FourD()
    assert len(result) > 100


def test_TOTO():
    result = draw_api.TOTO()
    assert len(result) > 100
