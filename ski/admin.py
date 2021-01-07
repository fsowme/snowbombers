from django.contrib import admin

from .models import (
    Airport,
    AirportDistance,
    Continent,
    Country,
    Lift,
    Resort,
    Slope,
)

admin.site.register(Airport)
admin.site.register(AirportDistance)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Lift)
admin.site.register(Resort)
admin.site.register(Slope)
