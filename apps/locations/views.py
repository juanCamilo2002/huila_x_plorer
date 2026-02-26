from django.db.models import Exists, OuterRef, Value, BooleanField
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from core.permissions import IsAdminRole
from .models import TouristSpot, TouristSpotImage, Favorite
from .serializers import TouristSpotSerializer, TouristSpotImageSerializer, FavoriteSerializer

class TouristSpotViewsSet(viewsets.ModelViewSet):
    serializer_class = TouristSpotSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'city', 'department']
    ordering_fields = ['created_at', 'name', 'is_featured']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = TouristSpot.objects.all()

        user = self.request.user
        if user.is_authenticated:
            fav_qs = Favorite.objects.filter(user=user, tourist_spot_id=OuterRef('pk'))
            qs = qs.annotate(is_favorite=Exists(fav_qs))
        else:
            qs = qs.annotate(is_favorite=Value(False, output_field=BooleanField()))

        city = self.request.query_params.get('city')
        department = self.request.query_params.get('department')
        featured = self.request.query_params.get('featured')
        category_id = self.request.query_params.get('category')

        if city:
            qs = qs.filter(city__iexact=city)
        if department:
            qs = qs.filter(department__iexact=department)
        if featured in ('true', '1', 'yes'):
            qs = qs.filter(is_featured=True)
        if category_id:
            qs = qs.filter(categories__id=category_id)
        
        return qs.distinct()
    
    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [AllowAny()]
        return [IsAdminRole()]

class TouristSoptImageViewSet(viewsets.ModelViewSet):
    serializer_class = TouristSpotImageSerializer

    def get_queryset(self):
        qs = TouristSpotImage.objects.select_related("spot").all()
        spot_id = self.request.query_params.get("spot")
        if spot_id:
            qs = qs.filter(spot_id=spot_id)
        return qs

    def get_permissions(self):
        # Lectura pública (si quieres), escritura solo ADMIN
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminRole()]

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)