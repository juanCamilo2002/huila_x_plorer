from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import BaseModel
from apps.users.models import User
from apps.locations.models import TouristSpot

class Review(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    tourist_spot = models.ForeignKey(
        TouristSpot,
        on_delete=models.CASCADE,
        related_name='reviews'   
    )

    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        db_table = "reviews"
        unique_together = ("user", "tourist_spot")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.tourist_spot.name}"

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_spot_rating(sender, instance, **kwargs):
    spot = instance.tourist_spot
    stats = spot.reviews.aggregate(
        avg=Avg('rating'),
        count=models.Count('id')
    )

    spot.average_rating = stats['avg'] or 0
    spot.reviews_count = stats['count']
    spot.save(update_fields=['average_rating', 'reviews_count'])