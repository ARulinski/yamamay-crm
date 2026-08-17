from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ("staff", "Staff"),
        ("manager", "Manager"),
        ("admin", "Administrator"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="staff",
    )

    store_name = models.CharField(
        max_length=150,
        blank=True,
    )

    def __str__(self):
        return self.get_full_name() or self.username