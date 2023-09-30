# recommendation/models.py

from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField()

class UserRequest(models.Model):
    prompt = models.TextField()
    recommended_movies = models.ManyToManyField(Movie)
