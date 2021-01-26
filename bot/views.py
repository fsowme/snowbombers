from random import randint, shuffle
from time import sleep

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import json
from ski.models import Continent, Country, Resort, Slope
from telegram import Update

from .handlers import BOT, DISPATCHER
from .models import User as django_user
from .parsers import get_regions, get_resort, get_resorts_soup


def check_user_start(user_data):
    user_id = int(user_data["id"])
    first_name = user_data["first_name"]
    is_bot = user_data["is_bot"]
    _, created = django_user.objects.get_or_create(
        telegram_id=user_id,
        defaults={"first_name": first_name, "is_bot": is_bot},
    )
    return created


@csrf_exempt
def webhook_updater(request):
    update = Update.de_json(json.loads(request.body), BOT)
    DISPATCHER.process_update(update)
    return HttpResponse("Ok")


def parse_continents(request):
    continents = get_regions()
    for continent in continents:
        Continent.objects.create(name=continent, url=continents[continent])
    return HttpResponse(continents)


def parse_countries(request):
    continents = Continent.objects.all()
    for continent in continents:
        sleep(randint(5, 10))
        countries = get_regions(region=continent.name)
        for country in countries:
            Country.objects.create(
                name=country, continent=continent, url=countries[country]
            )
    return HttpResponse(Country.objects.all())


def parse_resorts(request):
    countries = [
        country.name
        for country in Country.objects.all()
        if Resort.objects.filter(country=country).count() == 0
    ]
    countries = ["Austria", "France", "Italy", "Switzerland", "Russia", "USA"]
    shuffle(countries)
    for country in countries:
        resorts_soup = get_resorts_soup(country=country)
        if not resorts_soup:
            resorts_soup = get_resorts_soup(country=country, is_change_ip=True)
            if not resorts_soup:
                return HttpResponse(Resort.objects.all())
        sleep(randint(10, 100))
        for resort_soup in resorts_soup:
            resort_data = get_resort(resort_soup)
            if not resort_data:
                break
            if not Resort.objects.filter(name=resort_data["name"]):
                resort = Resort.objects.create(
                    name=resort_data["name"],
                    bottom_point=int(float(resort_data["bottom_point"])),
                    top_point=int(float(resort_data["top_point"])),
                    url=resort_data["url"],
                )
                Slope.objects.create(
                    resort=resort,
                    blue_slopes=int(float(resort_data["blue_slopes_length"])),
                    red_slopes=int(float(resort_data["red_slopes_length"])),
                    black_slopes=int(
                        float(resort_data["black_slopes_length"])
                    ),
                )
            else:
                resort = Resort.objects.get(name=resort_data["name"])
            Country.objects.get(name=country).resorts.add(resort)
    return HttpResponse(Resort.objects.all())
