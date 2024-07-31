from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Ride, RideEvent


class RideSerializer(serializers.ModelSerializer):
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
        ]


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id", "ride", "description", "created_at"]
