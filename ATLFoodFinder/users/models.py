from django.db import models
from django.contrib.auth.models import User

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rating = models.FloatField(null=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    google_maps_url = models.URLField(blank=True, null=True)
    place_id = models.CharField(max_length=255, unique=True)  # Add place_id

    def __str__(self):
        return self.name

class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()  # Assuming rating is on a scale of 1-5

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"

class GoogleReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return f"Google Review for {self.restaurant.name}"