import requests
from datetime import datetime as dt, timedelta


def get_default_user_group(auth_token) -> str:
    """

    :param auth_token:
    :return:
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
    :return: list of bitlink ids
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


def get_country_clicks(auth_token, bitlink, days=30, country=None):
    lookback_epoch = int((dt.now() - timedelta(days=days)).timestamp())
    response = requests.get(url=f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries",
                            headers={"Authorization": f"Bearer {auth_token}"})

    if response.status_code != 200:
        raise Exception