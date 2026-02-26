from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import Route, RouteStop
from .serializers import RouteSerializer, RouteStopSerializer
from .permissions import IsOwnerOrAdmin

class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.role == 'ADMIN':
                return Route.objects.all()
            return Route.objects.filter(
                Q(is_public=True) | Q(user=user)
            )
        return Route.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


class RouteStopViewSet(viewsets.ModelViewSet):
    serializer_class = RouteStopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RouteStop.objects.filter(route__user=self.request.user)

    def perform_create(self, serializer):
        route = serializer.validated_data["route"]

        if route.user != self.request.user:
            raise PermissionDenied("No puedes modificar esta ruta.")

        serializer.save()