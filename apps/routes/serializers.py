from rest_framework import serializers

from apps.locations.serializers import TouristSpotSerializer
from apps.locations.models import TouristSpot

from .models import Route, RouteStop

class RouteStopSerializer(serializers.ModelSerializer):
    tourist_spot_detail = TouristSpotSerializer(
        source='tourist_spot',
        read_only=True
    )

    class Meta:
        model = RouteStop
        fields = (
            'id',
            'tourist_spot',
            'tourist_spot_detail',
            'day',
            'order',
            'notes'
        )

        read_only_fields = ('id')


class RouteSerializer(serializers.ModelSerializer):
    stops = RouteStopSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = (
            'id',
            'name',
            'description',
            'days',
            'is_public',
            'stops',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
