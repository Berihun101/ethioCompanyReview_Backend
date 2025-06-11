from django.db import models
from category.models import Category
from django.db.models import Avg
from cloudinary.models import CloudinaryField

# Create your models here.



class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()
    logo = CloudinaryField('logo', folder='company_logos')

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        from review.models import Review # Import to avoid circular import
        return (
            Review.objects.filter(company=self).aggregate(Avg('rating'))['rating__avg'] or 0
        )
