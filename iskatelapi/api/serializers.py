from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault
from rest_framework_gis.fields import GeometryField 
from .models import Point, Messages

class PointSerializer(serializers.ModelSerializer):
    location = GeometryField()  
    
    class Meta:
        model = Point
        geo_field = 'location'
        fields = ('id', 'title', 'location', 'created_at')
        read_only_fields = ('id', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Messages
        fields = ("id", "message", "point", "created_at", "user")
        read_only_fields = ("id", "created_at")
        extra_kwargs = {"user": {"write_only": True}}
