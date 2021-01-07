import requests
from bs4 import BeautifulSoup

HOST = "https://www.ski.ru"
COUNTRIES = HOST + "/az/resorts"


SEARCH_PATH = HOST + "az/resorts/ajax_main_autocomplete"
TRACK_COLOR = ["green", "blue", "red", "black"]
TYPES_OF_LIFTS = {
    "ski-resort": "surface",
    "skiLift-resort": "chair",
    "wagon-resort": "cabin",
}


def get_page(url, params=""):
    response = requests.get(url=url, params=params)
    return response


def get_countries():
    countries_page = get_page(url=COUNTRIES)
    soup = BeautifulSoup(countries_page.text, "lxml")
    soup = soup.find_all(name="div", class_="countries")[0].find_all("a")
    countries = {}
    for country in soup:
        countries[country.text] = HOST + country.get("href")
    return countries


def resorts_by_country(country):
    country_url = get_countries()[country]
    country_page = get_page(url=country_url)
    soup = BeautifulSoup(country_page.text, "lxml")
    soup = soup.find_all(name="td", class_="curorts_table_tracks2")
    resorts = {}
    for resort in soup:
        resorts[resort.text] = HOST + resort.find("a").get("href")
    return resorts


# start = monotonic()
# print(get_countries())
# print(resorts_by_country("Италия"))
# print(monotonic() - start)
# def parse_resort_link(name):
#     data = {"q": name, "limit": 150}
#     response = requests.post(url=SEARCH_PATH, data=data)
#     link = response.text.split(sep="|")[-1].split(sep="\n")[0]
#     return link


# def parse_length_slopes(soup_content):
#     all_slopes = soup_content.find_all(name="ul", class_="length-tracks-list")
#     length_of_slopes = {}
#     for color in TRACK_COLOR:
#         slope_by_color = all_slopes[0].find(name="li", class_=color)
#         if slope_by_color:
#             length_of_slopes[color] = int(
#                 float(slope_by_color.text.split()[0])
#             )
#         else:
#             length_of_slopes[color] = 0
#     return length_of_slopes


# def parse_lifts(soup_content):
#     all_lifts = soup_content.find_all(name="ul", class_="lift-right-slopes")
#     lifts_by_type = {}
#     for lift_type in TYPES_OF_LIFTS:
#         amount_lifts = all_lifts[0].find("li", class_=lift_type)
#         if amount_lifts:
#             amount_lifts = int(amount_lifts.text)
#         else:
#             amount_lifts = 0
#         lifts_by_type[TYPES_OF_LIFTS[lift_type]] = amount_lifts
#     return lifts_by_type


# def parse_resort(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, features="lxml")
#     slope_length = parse_length_slopes(soup_content=soup)
#     lifts = parse_lifts(soup_content=soup)
#     return slope_length, lifts


# def start(part_of_name):
#     link = parse_resort_link(name=part_of_name)
#     print(parse_resort(url=link))


# start(part_of_name="Rosa Kh")
