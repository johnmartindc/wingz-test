from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from rides.constants import ROLE_CHOICES
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = None
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
