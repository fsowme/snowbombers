import json

from bs4 import BeautifulSoup

from bot.tor import ConnectionManager

HOST = "https://www.skiresort.info"
URL = "https://www.skiresort.info/ski-resorts{}/sorted/slope-length/"
SIMPLE_URL = "https://www.skiresort.info/ski-resorts/sorted/slope-length/"

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    # "pragma": "no-cache",
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "none",
    # "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
}

REGIONS = {
    "Earth": ["15022", ""],
    "Europe": ["34048", "/europe"],
    "North America": ["13568", "/north-america"],
    "South America": ["2525184", "/south-america"],
    "Asia": ["682496", "/asia"],
    "Australia and Oceania": ["115712", "/australia-and-oceania"],
    "Africa": ["1121280", "/africa"],
}


def get_page(url=HOST, headers=None, is_change_ip=False):
    headers = HEADERS if headers is None else headers
    connecion = ConnectionManager()
    if is_change_ip:
        connecion.new_identity()
    response = connecion.request(url=url, headers=HEADERS)
    return response


def get_region_json(url=None):
    url = HOST if url is None else url
    page = get_page(url=url)
    soup = BeautifulSoup(page.text, features="html5lib")
    scripts = soup.find_all("script")
    regions = [script.text for script in scripts if "var regions" in script.text][
        0
    ].strip()
    regions = json.loads(regions[regions.find("{") : regions.rfind("}") + 1])
    return regions["childs"]


def get_regions(region=None):
    region = "Earth" if region is None else region
    region_json = get_region_json(url=URL.format(REGIONS[region][1]))
    subregions = region_json[REGIONS[region][0]]["areas"]
    subregions = {
        subregion["name"]: subregion["url"] for subregion in subregions.values()
    }
    return subregions


def get_resorts_soup(country, is_change_ip=False):
    url = URL.format(f"/{country}")
    page = get_page(url=url, is_change_ip=is_change_ip)
    soup = BeautifulSoup(page.text, features="html5lib")
    soup = soup.find_all(
        "div",
        class_="panel panel-default resort-list-item resort-list-item-image--big",
    )
    return soup


def get_test_ip(is_change_ip=False):
    url = "https://2ip.ru"
    page = get_page(url=url, is_change_ip=is_change_ip)
    soup = BeautifulSoup(page.text, features="html5lib")
    soup = soup.find_all("div", class_="ip", id="d_clip_button")[0].text
    return soup


def get_resort(resort_soup):
    resort = {}
    name = " ".join(
        resort_soup.find("a", class_="h3").text.replace("/\u200b", "/").split()[1:]
    )
    url = resort_soup.find("a", class_="h3").get("href")
    if len(resort_soup.find_all("td")) < 8:
        return False

    height_difference, bottom_point, top_point = [
        height.text[:-2] for height in resort_soup.find_all("td")[2].find_all("span")
    ]
    all_slopes_length = resort_soup.find("span", class_="slopeinfoitem active")
    if all_slopes_length is not None:
        all_slopes_length = all_slopes_length.text[:-3]
    else:
        all_slopes_length = 0

    blue_slopes_length = resort_soup.find("span", class_="slopeinfoitem blue")
    if blue_slopes_length is not None:
        blue_slopes_length = blue_slopes_length.text[:-3]
    else:
        blue_slopes_length = 0

    red_slopes_length = resort_soup.find("span", class_="slopeinfoitem red")
    if red_slopes_length is not None:
        red_slopes_length = red_slopes_length.text[:-3]
    else:
        red_slopes_length = 0

    black_slopes_length = resort_soup.find("span", class_="slopeinfoitem black")
    if black_slopes_length is not None:
        black_slopes_length = black_slopes_length.text[:-3]
    else:
        black_slopes_length = 0

    amount_lifts = resort_soup.find("ul", class_="inline-dot").find("li")
    if amount_lifts is not None:
        amount_lifts = amount_lifts.text.split()[0]
    else:
        amount_lifts = 0

    resort = {
        "name": name,
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
    return resort
