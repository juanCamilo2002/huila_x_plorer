from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel
from apps.categories.models import Category

class TouristSpot(BaseModel):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField()


    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    categories = models.ManyToManyField(
        Category,
        related_name='spots',
        blank=True
    )

    main_image = models.ImageField(
        upload_to='locations/main/',
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(default=False)


    class Meta:
        db_table = 'tourist_spots'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=["department"]),
            models.Index(fields=["is_featured"]),
        ]
    
    def __str__(self):
        return self.name

class TouristSpotImage(BaseModel):
    spot = models.ForeignKey(
        TouristSpot,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='locations/images/')
    caption = models.CharField(max_length=200, blank=True)

    is_cover = models.BooleanField(default=False)
    order = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = 'tourist_spot_images'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['spot', 'is_cover']),
        ]
    
    def __str__(self):
        return f'{self.spot.name} - Image'