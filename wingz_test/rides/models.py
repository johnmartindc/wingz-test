from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from .constants import RIDE_STATUS_CHOICES
from users.models import CustomUser


class Ride(models.Model):
    status = models.CharField(max_length=30, choices=RIDE_STATUS_CHOICES)
    rider = models.ForeignKey(
        CustomUser, related_name="rider", on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        CustomUser, related_name="driver", on_delete=models.CASCADE
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def clean(self):
        if self.rider == self.driver:
            raise ValidationError("Driver and Rider cannot have the same value.")
        super().clean()

    def distance_to_pickup(self, input_latitude, input_longitude):
        input_point = Point(float(input_latitude), float(input_longitude))
        pickup_point = Point(self.pickup_latitude, self.pickup_longitude)
        distance = input_point.distance(pickup_point)  # in meters
        return distance


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
