import json

import requests
from bs4 import BeautifulSoup

HOST = "https://www.skiresort.info"


def get_page(url=HOST, params=""):
    response = requests.get(url=url, params=params)
    return response


def get_region_json(url):
    page = get_page(url=url)
    soup = BeautifulSoup(page.text, features="html5lib")
    scripts = soup.find_all("script")
    regions = [
        script.text for script in scripts if "var regions" in script.text
    ][0].strip()
    regions = json.loads(regions[regions.find("{") : regions.rfind("}") + 1])
    return regions


def get_continents(regions_json):
    continents = regions_json["childs"]["15022"]["areas"]
    continents = {
        region["name"]: region["url"] for region in continents.values()
    }
    return continents


def get_countries(continent: {"name": "url"}):
    page = get_page(continent["name"])
    soup = BeautifulSoup(page.text, features="html5lib")


print(get_continents(get_region_json(url=HOST)))
