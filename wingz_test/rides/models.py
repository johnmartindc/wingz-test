from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .constants import ROLE_CHOICES


class Role(models.Model):
    name = models.CharField(max_length=30, choices=ROLE_CHOICES)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    role = models.ManyToManyField(Role)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Ride(models.Model):
    status = models.CharField(max_length=30)
    rider = models.ForeignKey(User, related_name="rider", on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name="driver", on_delete=models.CASCADE)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def clean(self):
        # Ensure field1 and field2 are different
        if self.rider == self.driver:
            raise ValidationError("Driver and Rider cannot have the same value.")
        super().clean()


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
