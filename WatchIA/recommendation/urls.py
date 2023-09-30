# recommendation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('recommend_movies/', views.recommend_movies, name='recommend_movies'),
]
