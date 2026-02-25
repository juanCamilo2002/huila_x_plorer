from django.db import models
from django.utils.text import slugify
from core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name