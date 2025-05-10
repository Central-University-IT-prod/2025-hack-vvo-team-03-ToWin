from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    select_role = (
        (0, 'Игрок'),
        (1, 'Админ')
    )
    role = models.IntegerField(default=0, choices=select_role)
    command = models.BooleanField(default=1)
     