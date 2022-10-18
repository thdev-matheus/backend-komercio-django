from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
