"""
Views for image apis
"""

import requests
import os

from rest_framework.decorators import (
    action,
    api_view
)

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


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

# ===============================================================================
#  Function-based views for custom endpoints
# ===============================================================================


@api_view(['POST'])
def update_status(request):
    hotspot_id = request.data.get('id',[])
    new_status = request.data.get('status',[])
    Hotspot

    distinct_paths = Location.objects.values_list('path_id', flat=True).distinct()
    return Response(distinct_paths, status=status.HTTP_200_OK)    

@api_view(['GET'])
def get_distinct_path_ids(request):
    distinct_paths = Location.objects.values_list('path_id', flat=True).distinct()
    return Response(distinct_paths, status=status.HTTP_200_OK)    

@api_view(['GET'])
@extend_schema(
    description = "Endpoint for getting location data ",
    parameters = [
        OpenApiParameter(
            'path_id',
            OpenApiTypes.INT,
            description='the id of the path',
            required = False
        ),
    ]
)
def get_locations_data_by_path(request):
    """API for retrieving location data based on path_id"""
    path_id = int(request.query_params.get('path_id'))

    if not path_id:
        return Response('no path_id provided',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    locations = Location.objects.filter(path_id=path_id)
    if not locations:
        return Response(f'path id doesnt exist {path_id}',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    print(f'locations: {locations}')

    response_data = []
    for location in locations:
        print(ImageRecord.objects.filter(location=location).order_by('-date'))
        # since there is only one record the latest record is the only one for that location
        records = ImageRecord.objects.filter(location=location).order_by('-date')
        if not records.exists():
            return Response(f'no records for this location {location}',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        record = records[0]
        print(f'record: {record}')
        print(f'hotspot objects: {[x.record for x in Hotspot.objects.all()]}')
        print("-----------------")
        hotspot = Hotspot.objects.filter(record=record)
        is_hotspot = hotspot.exists()

        hotspot_size = 0
        hotspot_status = 'no status'
        hotspot_id = -1
        if is_hotspot:
            hotspot_id = hotspot[0].id
            hotspot_size = hotspot[0].size
            hotspot_status = hotspot[0].status

        # TODO: get image path

        location_dict = {
            'id' : location.id,
            'x' : location.x,
            'y' : location.y,
            'path_id': location.path_id,
            'date': record.date,
            'ir_image_path': record.image_ir.url,
            'rgb_image_path': record.image_rgb.url,
            'is_hotspot': is_hotspot,
            'hotspot_id': hotspot_id,
            'size' : hotspot_size,
            'status' : hotspot_status,
        }
        response_data.append(location_dict)

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@extend_schema(
    description='Endpoint to call when uploading record (from drone)',
)
def add_record(request, format='json'):
    """API for adding record"""
    data = request.data
    x = float(data.pop('x_coord',[])[0])
    y = float(data.pop('y_coord',[])[0])
    path_id = float(data.pop('path_id',[])[0])

    # get or create location
    location_obj, created = Location.objects.get_or_create(x=x,y=y,path_id=path_id)
    data['location'] = location_obj.id

    serializer = serializers.ImageRecordSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ===============================================================================
#  Viewsets for models
# ===============================================================================

class ImageRecordViewSet(viewsets.ModelViewSet):
    """View for managing image api's"""
    serializer_class = serializers.ImageRecordSerializer
    queryset = ImageRecord.objects.all()    

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
            return self.queryset.filter(path_id=path_id_int)
        
        return self.queryset
    
class HotspotViewSet(viewsets.ModelViewSet):
    """View for managing Hotspot api"""
    serializer_class = serializers.HotspotSerializer
    queryset = Hotspot.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'update_status':
            return serializers.HotspotStatusSerializer
        
        return self.serializer_class


    @action(methods=['POST'], detail=True, url_path='update-status')
    def update_status(self, request, pk=None):
        """Upload an image to recipe"""
        hotspot = self.get_object()
        serializer = self.get_serializer(hotspot, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
