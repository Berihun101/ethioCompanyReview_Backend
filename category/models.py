from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)

    def __str__(self):
        return self.name