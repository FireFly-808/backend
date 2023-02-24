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
        fields = ['id','type','location','date','image']
        read_only_fields = ['id']
        extra_kwargs = {'image':{'required':'True'}}

class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location records"""

    class Meta:
        model = Location
        fields = ['id','x','y']
        read_only_fields = ['id']



class HotspotSerializer(serializers.ModelSerializer):
    """Serializer for Hotspot records"""

    class Meta:
        model = Hotspot
        fields = ['id','location','size','status']
        read_only_fields = ['id']
