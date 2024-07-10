from rest_framework import serializers
from rest_framework.exceptions import status, ValidationError
from .models import User, Ride, RideEvent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_number", "role"]


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
