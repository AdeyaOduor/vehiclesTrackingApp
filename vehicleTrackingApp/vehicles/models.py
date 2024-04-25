from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    make = models.CharField(max_length=255)

    class Meta:
        ordering = ('make',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.make

class Vehicle(models.Model):
    category = models.ForeignKey(Category, related_name='vehicles', on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    registration = models.CharField(max_length=50)
    image = models.ImageField(upload_to='vehicles_images', blank=True, null=True)
    is_ticketed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='vehicles', on_delete=models.CASCADE)