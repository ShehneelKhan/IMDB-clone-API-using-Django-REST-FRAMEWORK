from watchlist_app.models import WatchList, StreamPlatform, Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        #fields = '__all__'
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.StringRelatedField(source='platform.name', read_only=True)
    
    class Meta:
        model = WatchList 
        fields = '__all__'
        #fields = ['id','name']
       
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
        
