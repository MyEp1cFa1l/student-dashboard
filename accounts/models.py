from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь. Пока расширяем только полем 'university'."""

    university = models.CharField(max_length=200, blank=True)
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username