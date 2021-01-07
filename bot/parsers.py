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
