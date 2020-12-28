from django.contrib import admin

from .models import (
    Airport,
    AirportDistance,
    Country,
    Lift,
    Region,
    Resort,
    Slope,
)

admin.site.register(Airport)
admin.site.register(AirportDistance)
admin.site.register(Country)
admin.site.register(Lift)
admin.site.register(Region)
admin.site.register(Resort)
admin.site.register(Slope)
