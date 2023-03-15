from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly, IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


        
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset:
            raise ValidationError('You cannot create a review more than once')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        
        watchlist.number_rating += 1
        watchlist.save()
                    
        serializer.save(watchlist=watchlist, review_user=review_user)



class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['avg_rating', 'number_rating']
    filterset_fields = ['title', 'active']
        
class WatchListList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        if not movies:
            return Response({'message': 'Objects does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movies, many=True)     # Since there are multiple objects, we will user many=True otherwise error will come
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
            
class WatchDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)  
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class StreamPlatformList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        if not platforms:
            return Response({'message': 'Objects does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class StreamPlatformDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'message': 'Does not exist'}, status=status.HTTP_404_NOT_FOUND)        
        platform.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

  
        


        
    
   
        
        

       
    