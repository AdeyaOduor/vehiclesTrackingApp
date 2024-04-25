from django.db import models

class Category(models.Model):
    make = models.CharField(max_length=100)

    def __str__(self):
        return self.make

class Vehicle(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_ticketed = models.BooleanField(default=False)

    def __str__(self):
        return self.make