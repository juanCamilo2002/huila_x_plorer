from rest_framework import serializers
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from .models import TouristSpot, TouristSpotImage


class TouristSpotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristSpotImage
        fields = ("id", "spot", "image", "caption", "is_cover", "order", "created_at")
        read_only_fields = ("id", "created_at")


class TouristSpotSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    images = TouristSpotImageSerializer(many=True, read_only=True)

    class Meta:
        model = TouristSpot
        fields = (
            "id",
            "name",
            "short_description",
            "description",
            "address",
            "city",
            "department",
            "latitude",
            "longitude",
            "is_featured",
            "main_image",
            "categories",
            "category_ids",
            "images",
            "average_rating",
            "reviews_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id", 
            "created_at", 
            "updated_at", 
            "categories", 
            "images",
            "average_rating",
            "reviews_count",
        )

    def _set_categories(self, spot: TouristSpot, category_ids):
        if category_ids is None:
            return
        qs = Category.objects.filter(id__in=category_ids)
        spot.categories.set(qs)

    def create(self, validated_data):
        category_ids = validated_data.pop("category_ids", None)
        spot = super().create(validated_data)
        self._set_categories(spot, category_ids)
        return spot

    def update(self, instance, validated_data):
        category_ids = validated_data.pop("category_ids", None)
        spot = super().update(instance, validated_data)
        self._set_categories(spot, category_ids)
        return spot