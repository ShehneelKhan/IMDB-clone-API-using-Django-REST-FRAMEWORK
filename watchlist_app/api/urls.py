from django.urls import path
from .views import MovieList, MovieDetail


urlpatterns = [
    path('movie/list/', MovieList.as_view(), name='movie_list'),
    path('movie/<int:pk>', MovieDetail.as_view(), name='movie_detail'),
    
]
