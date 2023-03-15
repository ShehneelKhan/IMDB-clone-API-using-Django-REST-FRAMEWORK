from django.urls import path
from .views import WatchListList, WatchListGV, WatchDetail, StreamPlatformList, StreamPlatformDetail, ReviewList, ReviewDetail, ReviewCreate


urlpatterns = [
    path('list/', WatchListList.as_view(), name='watch_list'),
    path('list2/', WatchListGV.as_view(), name='watch_list2'),
    path('<int:pk>/', WatchDetail.as_view(), name='watch_detail'),
    path('', StreamPlatformList.as_view(), name='stream_list'),
    path('<int:pk>/', StreamPlatformDetail.as_view(), name='stream_detail'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
]
