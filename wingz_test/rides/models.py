from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Role(models.Model):
    name = models.CharField(max_length=30)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    role = models.ManyToManyField(Role)


class Ride(models.Model):
    status = models.CharField(max_length=30)
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
