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

from server import serializers

@extend_schema_view(
    description='Endpoint to call when uploading record (from drone)',
)
class ImageRecordApiView(APIView):
    """API for managing image records"""

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

class ImageRecordViewSet(viewsets.ModelViewSet):
    """View for managing image api's"""
    serializer_class = serializers.ImageRecordSerializer
    queryset = ImageRecord.objects.all()    

    # def get_serializer_class(self):
    #     """Return the serializer class for request"""
    #     if self.action == 'add_custom_record':
    #         return serializers.CustomImageRecordSerializer
        
    #     return self.serializer_class


    @action(methods=['POST'], detail=False, url_path='add-custom-record')
    def add_custom_record(self, request, pk=None):
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
    
    @extend_schema(
        parameters = [
            OpenApiParameter(
                'loc_id',
                OpenApiTypes.INT,
                description='the id of the location',
                required = True
            ),
        ]
    )    
    @action(methods=['GET'], detail=False, url_path='get-record-pair')
    def get_record_pair(self,request,pk=None):
        """Retrieve pair of records for specified location"""
        loc_id = int(self.request.query_params.get('loc_id'))
        loc = Location.objects.get(id=loc_id)

        record_ir = ImageRecord.objects.filter(location=loc, type='ir').order_by('-date')[:1][0]
        record_rgb = ImageRecord.objects.filter(location=loc, type='rgb').order_by('-date')[:1][0]

        if record_rgb.type == record_ir.type:
            return Response('records of same type',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # hotspot = Hotspot.objects.get(location=loc)
    
        # TODO: HOW TO RETURN IMAGE
        data = {
            'ir_image': 1, #record_ir.image,
            'rgb_image': 1,#record_rgb.image,
            'date':record_ir.date,
            'is_hotspot': True,
            'size' : 1,
            'status' : 'hella bad'
        }

        return Response(data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        parameters = [
            OpenApiParameter(
                'path_id',
                OpenApiTypes.INT,
                description='the id of the path',
                required = False
            ),
        ]
    )
)
class LocationViewSet(viewsets.ModelViewSet):
    """View for managing location api"""
    serializer_class = serializers.LocationSerializer
    queryset = Location.objects.all()

    def get_queryset(self):
        """Retrieve locations"""
        path_id = self.request.query_params.get('path_id')
        if path_id:
            path_id_int = int(path_id)
            return self.queryset.filter(path=path_id_int)
        
        return self.queryset
    


    
class HotspotViewSet(viewsets.ModelViewSet):
    """View for managing Hotspot api"""
    serializer_class = serializers.HotspotSerializer
    queryset = Hotspot.objects.all()