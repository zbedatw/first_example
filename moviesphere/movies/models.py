from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# Movie model
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    director = models.CharField(max_length=30)
    actors = models.TextField()
    year = models.CharField(max_length=4)
    thumb = models.ImageField(default='default.jpg',blank=True)
    trailer_url = models.URLField(max_length=200, blank=True, null=True)

    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating else 0

    def __str__(self):
        return self.title

# Review model
class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rate 1-5
    comment = models.TextField()

    class Meta:
        unique_together = ('movie', 'user')  # Ensure one review per user per movie

    def __str__(self):
        return f'{self.user.username} review on {self.movie.title}'