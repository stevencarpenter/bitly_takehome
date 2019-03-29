import requests
from datetime import datetime as dt, timedelta


def get_default_user_group(auth_token) -> str:
    """

    :param auth_token: bitly auth token
    :return: string for the default_group_guid
    """

    response = requests.get(url="https://api-ssl.bitly.com/v4/user",
                            headers={"Authorization": f"Bearer {auth_token}"})
    if response.status_code != 200:
        raise Exception
    return response.json()["default_group_guid"]


def get_bitlinks(auth_token, group_guid) -> list:
    """

    :param auth_token: bitly auth token
    :param group_guid: bitly group_id to get links for
    :return: list of bitlink ids that are a part of the default_group_guid
    """
    response = requests.get(url=f"https://api-ssl.bitly.com/v4/groups/{group_guid}/bitlinks?size=1",
                            headers={"Authorization": f"Bearer {auth_token}"})

    if response.status_code != 200:
        raise Exception

    pages = response.json()["pagination"]["total"]
    if pages == 1:
        return [link["id"] for link in response.json()["links"]]
    else:
        links = []
        links.extend([link["id"] for link in response.json()["links"]])
        for page in range(1, pages):
            next_page = response.json()["pagination"]["next"]
            response = requests.get(next_page, headers={"Authorization": f"Bearer {auth_token}"})
            links.extend([link["id"]
                          for link in response.json()["links"]])
        return links


def get_country_clicks(auth_token, bitlink, unit,  units=30) -> dict:
    """
    Takes a bitlink and params to determine lookback period and returns
    a dictionary of countries and thier click totals.

    :param auth_token: bitly auth token
    :param bitlink: bitlink id which is the url without the https://
    :param unit: unit of time for the lookback units. Must be a member of
                 unit_enum list defined below.
    :param units: number of units to look back. Must be greater than -1
    :return: dictionary of {country: clicks}
    """

    unit = unit.lower()
    unit_enum = ["minute", "hour", "day", "week", "month"]
    assert unit in unit_enum, "Value provided for unit is invalid."
    assert units >= -1, "Value provided for units must be -1 for all time or greater."

    response = requests.get(url=f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries?unit={unit}&units={units}",
                            headers={"Authorization": f"Bearer {auth_token}"})

    if response.status_code != 200:
        raise Exception("Non 200 error code received from bitly endpoint.")

    return {d["value"]: d["clicks"] for d in list(response.json()["metrics"])}



