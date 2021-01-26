from django.db import models
from ski.models import Resort


class User(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=50)
    bookmarks = models.ManyToManyField(
        Resort,
        related_name="followers",
        verbose_name="Закладки пользователя",
    )
