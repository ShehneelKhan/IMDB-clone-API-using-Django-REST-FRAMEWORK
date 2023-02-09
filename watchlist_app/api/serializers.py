from watchlist_app.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    
    len_name = serializers.SerializerMethodField() # For those fields, we want in our API's but we don't have them in our models(Most likely used for calculation of something)
    
    class Meta:
        model = Movie
        fields = '__all__'
        #fields = ['id','name']
        #exclude = ['active']
        
    def get_len_name(self, object):
        return len(object.name)
        
    def validate_name(self, value): #Field level validation
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value
    
    def validate(self, data): #Object level validation
        if data['name'] == data['description']:
            raise serializers.ValidationError("Title and description cannot be the same")
        return data    
