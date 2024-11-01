from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from django.db.models import Avg

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    released_at = models.DateField()
    duration_hours = models.PositiveIntegerField(default=0) 
    duration_minutes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])  # Minutes
    duration_seconds = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])  # Seconds
    genre = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.rating_set.all()  
        if ratings.exists():
            return ratings.aggregate(Avg('rating'))['rating__avg']  
        return 0.0  

    def total_ratings(self):
        return self.rating_set.count()  

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reason = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user.username} reported {self.movie.title}"