from watchlist_app.models import Movie
from rest_framework import serializers

def name_length(value): #Validation through validators
    if len(value) < 2:
        raise serializers.ValidationError("Name must be at least 2 characters long")
    return value


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length], max_length=100)  #Here is the validators argument that is used for the function above
    description = serializers.CharField(max_length=1000)
    active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    # def validate_name(self, value): #Field level validation
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name must be at least 2 characters long")
    #     return value
    
    def validate(self, data): #Object level validation
        if data['name'] == data['description']:
            raise serializers.ValidationError("Title and description cannot be the same")
        return data    
