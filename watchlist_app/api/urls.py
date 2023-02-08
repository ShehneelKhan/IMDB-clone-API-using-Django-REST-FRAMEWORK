from django.urls import path
from .views import movie_list, movie_detail


urlpatterns = [
    path('movie/list/', movie_list, name='movie_list'),
    path('movie/<int:pk>', movie_detail, name='movie_detail'),
    
]
