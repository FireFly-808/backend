"""
Views for image apis
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import(
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status
)

from core.models import (
    ImageRecord,
    Location,
    Hotspot
)

from record import serializers

@extend_schema_view(
    summary='API for uploading images to the database',
)
class ImageRecordApiView(APIView):
    """API for managing image records"""

    # @extend_schema(
    #     request={
    #         "type": "object",
    #         "properties": {
    #             "type": {"type": "string"},
    #             "x_coord": {"type": "number"},
    #             "y_coord": {"type": "number"},
    #             "date": {"type": "string", 'format':'date'},
    #             "image": {
    #                 "type": "string",
    #                 "format": "binary",
    #                 "description": "The image file to upload."
    #             }
    #         },
    #         "required": ["type","x_coord","y_coord","date","image"]
    #     },
    #     responses={status.HTTP_200_OK: {"type": "string"}}
    # )
    def post(self, request, format='json'):
        """Adds image record to db"""
        data = request.data
        x = float(data.pop('x_coord',[])[0])
        y = float(data.pop('y_coord',[])[0])

        # get or create location
        location_obj, created = Location.objects.get_or_create(
            x = x,
            y = y
        )

        data['location'] = location_obj.id

        serializer = serializers.ImageRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LocationApiView(APIView):

class ImageRecordViewSet(viewsets.ModelViewSet):
    """View for managing image api's"""
    serializer_class = serializers.ImageRecordSerializer
    queryset = ImageRecord.objects.all()

    def get_serializer_class(self):
        """Determine serializer for this request"""
        if self.action == 'upload_image':
            return serializers.ImageRecordSerializer

        return self.serializer_class

class LocationViewSet(viewsets.ModelViewSet):
    """View for managing location api"""
    serializer_class = serializers.LocationSerializer
    queryset = Location.objects.all()
    
class HotspotViewSet(viewsets.ModelViewSet):
    """View for managing Hotspot api"""
    serializer_class = serializers.HotspotSerializer
    queryset = Hotspot.objects.all()
    
    





    