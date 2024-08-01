from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Ride, RideEvent
from django.utils import timezone
from datetime import timedelta


class RideSerializer(serializers.ModelSerializer):
    todays_ride_events = serializers.SerializerMethodField()

    def get_todays_ride_events(self, obj):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)
        recent_events = obj.ride_events.filter(created_at__gte=last_24_hours)
        return RideEventSerializer(recent_events, many=True).data

    def validate(self, data):
        instance = Ride(**data)
        try:
            instance.clean()
            return data
        except ValidationError as e:
            raise serializers.ValidationError(e.args[0])

    class Meta:
        model = Ride
        fields = [
            "id",
            "status",
            "rider",
            "driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "todays_ride_events",
        ]


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id", "ride", "description", "created_at"]
