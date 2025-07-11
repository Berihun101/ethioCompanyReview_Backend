from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    icon = CloudinaryField(
        'icon', 
        folder='media/category_icons',  # Organized folder structure
        transformation={'quality': 'auto:good'},  # Optional optimization
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        if self.icon:
            return self.icon.url
        return None