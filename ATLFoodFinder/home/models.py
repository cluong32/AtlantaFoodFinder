from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cuisine_type = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
