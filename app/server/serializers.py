"""
Serializers for the record api
"""

from rest_framework import serializers
from core.models import (
    ImageRecord,
    Location,
    Hotspot,
)

class ImageRecordSerializer(serializers.ModelSerializer):
    """Serializer for Image records"""

    class Meta:
        model = ImageRecord
        fields = ['id','location','date','image_ir','image_rgb']
        read_only_fields = ['id']
        extra_kwargs = {'image_rgb':{'required':'True'},'image_ir':{'required':'True'}}

# class CustomImageRecordSerializer(serializers.Serializer):
#     """Serializer for drone api call"""
#     type = serializers.CharField()
#     x_coord = serializers.FloatField()
#     y_coord = serializers.FloatField()
#     date = serializers.DateTimeField()
#     image = serializers.ImageField()
    
class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location records"""

    class Meta:
        model = Location
        fields = ['id','x','y','path_id']
        read_only_fields = ['id']



class HotspotSerializer(serializers.ModelSerializer):
    """Serializer for Hotspot records"""

    class Meta:
        model = Hotspot
        fields = ['id','record','size','status']
        read_only_fields = ['id']

class HotspotStatusSerializer(serializers.ModelSerializer):
    """Serializer for Hotspot records"""

    class Meta:
        model = Hotspot
        fields = ['id','status']
        read_only_fields = ['id']
