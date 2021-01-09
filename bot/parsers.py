import json
from time import monotonic

import requests
from bs4 import BeautifulSoup

HOST = "https://www.skiresort.info"
URL = "https://www.skiresort.info/ski-resorts{}/sorted/slope-length/"

REGIONS = {
    "Earth": ["15022", ""],
    "Europe": ["34048", "/europe"],
    "North America": ["13568", "/north-america"],
    "South America": ["2525184", "/south-america"],
    "Asia": ["682496", "/asia"],
    "Australia and Oceania": ["115712", "/australia-and-oceania"],
    "Africa": ["1121280", "/africa"],
}


def get_page(url=HOST, params=""):
    response = requests.get(url=url, params=params)
    return response


def get_region_json(url=None):
    url = HOST if url is None else url
    page = get_page(url=url)
    soup = BeautifulSoup(page.text, features="html5lib")
    scripts = soup.find_all("script")
    regions = [
        script.text for script in scripts if "var regions" in script.text
    ][0].strip()
    regions = json.loads(regions[regions.find("{") : regions.rfind("}") + 1])
    return regions["childs"]


def get_regions(region=None):
    region = "Earth" if region is None else region
    region_json = get_region_json(url=URL.format(REGIONS[region][1]))
    subregions = region_json[REGIONS[region][0]]["areas"]
    subregions = {
        subregion["name"]: subregion["url"]
        for subregion in subregions.values()
    }
    return subregions


def get_resorts(country):
    url = URL.format(f"/{country}")
    page = get_page(url=url)
    soup = BeautifulSoup(page.text, features="html5lib")
    soup = soup.find_all(
        "div",
        class_="panel panel-default resort-list-item resort-list-item-image--big",
    )
    resorts = {}
    for resort in soup:
        name = " ".join(
            resort.find("a", class_="h3")
            .text.replace("/\u200b", "/")
            .split()[1:]
        )
        url = resort.find("a", class_="h3").get("href")
        height_difference, bottom_point, top_point = [
            height.text[:-2]
            for height in resort.find_all("td")[2].find_all("span")
        ]
        all_slopes_length = resort.find(
            "span", class_="slopeinfoitem active"
        ).text[:-3]

        blue_slopes_length = resort.find(
            "span", class_="slopeinfoitem blue"
        ).text[:-3]

        red_slopes_length = resort.find(
            "span", class_="slopeinfoitem red"
        ).text[:-3]

        black_slopes_length = resort.find(
            "span", class_="slopeinfoitem black"
        ).text[:-3]
        amount_lifts = (
            resort.find("ul", class_="inline-dot").find("li").text.split()[0]
        )
        resorts[name] = {
            "url": url,
            "height_difference": height_difference,
            "bottom_point": bottom_point,
            "top_point": top_point,
            "all_slopes_length": all_slopes_length,
            "blue_slopes_length": blue_slopes_length,
            "red_slopes_length": red_slopes_length,
            "black_slopes_length": black_slopes_length,
            "amount_lifts": amount_lifts,
        }
    return resorts


if __name__ == "__main__":

    start = monotonic()
    # print(get_regions("Europe"))
    print(get_resorts("Italy"))
    print(monotonic() - start)
