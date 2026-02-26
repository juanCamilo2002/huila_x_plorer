from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id',
            'tourist_spot',
            'rating',
            'comment',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating debe estar entre 1 y 5.')
        return value