from app.bitly_api_functions import *


def test_flatten_clicks_single_country():
    clicks_data = [
        {
            "value":  "US",
            "clicks": 3
        }
    ]
    expected_result = {"US": 3}
    actual_result = flatten_clicks(clicks_data)
    assert actual_result == expected_result


def test_flatten_clicks_many_countries():
    clicks_data = [
        {
            "value":  "US",
            "clicks": 3
        },
        {
            "value":  "UK",
            "clicks": 3
        }, {
            "value":  "BR",
            "clicks": 3
        }
        , {
            "value":  "RU",
            "clicks": 3
        }
        , {
            "value":  "FR",
            "clicks": 3
        }
    ]
    expected_result = {"US": 3, "UK": 3, "BR": 3, "RU": 3, "FR": 3}
    actual_result = flatten_clicks(clicks_data)
    assert actual_result == expected_result


def test_average_clicks_per_country():
    bitlinks = {"US": 2}
    expected_result = {"US": 1}
    actual_result = average_clicks_per_country(bitlinks, 2)
    assert actual_result == expected_result


def test_average_clicks_per_many_countries():
    bitlinks = {"US": 2, "UK": 4, "BR": 6, "RU": 8}
    expected_result = {"US": 1, "UK": 2, "BR": 3, "RU": 4}
    actual_result = average_clicks_per_country(bitlinks, 2)
    assert actual_result == expected_result
