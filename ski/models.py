import uuid
from uuid import uuid4

from django.db import models
from django.db.models import F


class Continent(models.Model):
    name = models.CharField(
        max_length=50, unique=True, verbose_name="Часть света"
    )
    url = models.SlugField(unique=True, verbose_name="Continent url")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name="Страна")
    continent = models.ForeignKey(
        Continent,
        on_delete=models.PROTECT,
        related_name="countries",
        verbose_name="Часть света",
    )
    url = models.SlugField(verbose_name="Country url")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Название аэропорта"
    )
    iata_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Сокращеное имя по ИАТА",
        blank=True,
        null=True,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="airports",
        verbose_name="Страна аэропорта",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Resort(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Курорт")
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Уникальное имя (32 бита)",
    )
    country = models.ManyToManyField(
        Country, related_name="resorts", verbose_name="Сатраны"
    )
    skipass_price = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Цена скипасса"
    )

    bottom_point = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Нижняя точка"
    )
    top_point = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Верхняя точка"
    )
    url = models.SlugField(unique=True, verbose_name="Resort url")

    class Meta:
        ordering = [
            -F("slopes__blue_slopes")
            - F("slopes__red_slopes")
            - F("slopes__black_slopes")
        ]

    def height_difference(self):
        return self.top_point - self.bottom_point

    def __str__(self):
        return self.name


class Slope(models.Model):
    resort = models.OneToOneField(
        Resort,
        on_delete=models.CASCADE,
        related_name="slopes",
        verbose_name="Курорт",
    )

    green_slopes = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Протяжённость зелёных трасс"
    )
    blue_slopes = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Протяжённость синих трасс"
    )
    red_slopes = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Протяжённость красных трасс"
    )
    black_slopes = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Протяжённость чёрных трасс"
    )

    class Meta:
        ordering = [-F("blue_slopes") - F("red_slopes") - F("black_slopes")]

    @property
    def all_slopes(self):
        return sum(
            [
                # self.green_slopes,
                self.blue_slopes,
                self.red_slopes,
                self.black_slopes,
            ]
        )

    def __str__(self):
        return f"Трассы {self.resort}"


class Lift(models.Model):
    resort = models.OneToOneField(
        Resort,
        on_delete=models.CASCADE,
        related_name="lifts",
        verbose_name="Курорт",
    )
    gondola_tram = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Количество гондол"
    )
    chairs = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Кресельные подъемники"
    )
    surface = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Бугели"
    )

    def all_lifts(self):
        return sum([self.gondola_tram, self.chairs, self.surface])

    def __str__(self):
        return f"Подъёмники {self.resort}"


class AirportDistance(models.Model):
    distance = models.PositiveSmallIntegerField(
        verbose_name="Расстояние от аэропорта до курорта"
    )
    airport = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="distances",
        verbose_name="Аэропорт",
    )
    resort = models.ForeignKey(
        Resort,
        on_delete=models.PROTECT,
        related_name="airport_distances",
        verbose_name="Куррорт",
    )

    def __str__(self):
        return f"{self.resort} - {self.airport}: {self.distance}"
