from django.db import models
from core.models import BaseModel
from apps.users.models import User
from apps.locations.models import TouristSpot

class Route(BaseModel):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='routes'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    days = models.PositiveIntegerField(default=1)

    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = 'routes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.user.email}'

class RouteStop(BaseModel):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='stops'
    )

    tourist_spot = models.ForeignKey(
        TouristSpot,
        on_delete=models.CASCADE,
        related_name='route_stops'
    )

    day = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)

    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'route_stops'
        ordering = ['day', 'order']
        unique_together = ('route', 'day', 'order')
    
    def __str__(self):
        return f'{self.route.name} - {self.tourist_spot.name}'