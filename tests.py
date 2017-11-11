from promos import api as promo_api
from draws import api as draw_api
from train_alert import api as train_api
from gov import api as gov_api

# Testing Promo APIs

def test_get_promos():
    result = promo_api.get_promos('https://www.couponese.com/store/uber.com/')
    assert isinstance(result, dict)


def test_promo_loop():
    result = promo_api.promo_loop('{"uber":"https://www.couponese.com/store/uber.com/"}')
    assert isinstance(result, str)
    assert len(result) > 20


# Testing Draw API

def test_FourD():
    result = draw_api.FourD()

    # Checking Length of Result
    assert len(result) > 100

    # Checking Basic Struture of Response
    assert "Consolation Prizes" in result
    assert "Special/Starter Prizes" in result
    assert "1st -" in result


def test_TOTO():
    result = draw_api.Toto()

    # Checking Length of Result
    assert len(result) > 100

    # Checking Basic Struture of Response
    assert "Winning Numbers" in result
    assert "Bonus" in result

# Testing Train Alert API

def test_train_alert():
    result = train_api.connect_twitter_api()
    assert len(result) == 5

    result = train_api.connect_twitter_api("@SBSTransit_Ltd")
    assert len(result) == 5

# Testing Weather API

def test_weathermap():
    result = gov_api.weather_get()
    assert "https://pbs.twimg.com/media/" in result
