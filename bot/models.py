from django.db import models


class User(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=50)
