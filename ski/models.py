from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Страна")
    visa = models.BooleanField(verbose_name="Требуется виза")
    currency = models.CharField(max_length=30, verbose_name="Местная валюта")

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Регион")
    country = models.ManyToManyField(
        Country, related_name="regions", verbose_name="Страна региона"
    )

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Название аэропорта"
    )
    iata_code = models.CharField(
        max_length=10, unique=True, verbose_name="Сокращеное имя по ИАТА"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="airports",
        verbose_name="Страна аэропорта",
    )

    def __str__(self):
        return self.name


class Resort(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Курорт")
    country = models.ManyToManyField(
        Country, related_name="resorts", verbose_name="Страна курорта"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="resorts",
        verbose_name="Регион",
        blank=True,
        null=True,
    )
    airport = models.ManyToManyField(
        Airport, related_name="resorts", verbose_name="Ближайшие аэропорты"
    )
    skipass_price = models.PositiveSmallIntegerField(
        verbose_name="Цена скипасса"
    )

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
        verbose_name="Протяжённость зелёных трасс"
    )
    blue_slopes = models.PositiveSmallIntegerField(
        verbose_name="Протяжённость синих трасс"
    )
    red_slopes = models.PositiveSmallIntegerField(
        verbose_name="Протяжённость красных трасс"
    )
    black_slopes = models.PositiveSmallIntegerField(
        verbose_name="Протяжённость чёрных трасс"
    )

    def all_slopes(self):
        return sum(
            [
                self.green_slopes,
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
