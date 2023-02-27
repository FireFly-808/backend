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
)

from server import serializers

# ===============================================================================
#  Function-based views for custom endpoints
# ===============================================================================

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
    # print(f'locations: {locations}')

    response_data = []
    for location in locations:
        # print(ImageRecord.objects.filter(location=location).order_by('-date'))
        # since there is only one record the latest record is the only one for that location
        records = ImageRecord.objects.filter(location=location).order_by('-date')
        if not records.exists():
            return Response(f'no records for this location {location}',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        record = records[0]

        location_dict = {
            'loc_id' : location.id,
            'x' : location.x,
            'y' : location.y,
            'path_id': location.path_id,
            'record_id':record.id,
            'date': record.date,
            'ir_image_path': record.image_ir.url,
            'rgb_image_path': record.image_rgb.url,
            'is_hotspot': record.is_hotspot,
            'status' : record.status,
        }
        response_data.append(location_dict)

    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def update_status(request, pk=None):
#     """Upload an image to recipe"""
#     data = request.data
#     loc_id = data.pop('loc_id',[])
#     loc = Location.objects.get(id=loc_id)
#     record = ImageRecord.objects.get(location=loc)

#     serializer = serializers.StatusSerializer(record, data=data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

    serializer = serializers.ImageRecordUploadSerializer(data=data)
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

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'update_status':
            return serializers.StatusSerializer
        elif self.action == 'get_unclassified_records':
            return serializers.UnclassifiedRecordSerializer
        elif self.action == 'send_classification':
            return serializers.NewClassificationSerializer
        
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='update_status')
    def update_status(self, request, pk=None):
        """Update status of record"""

        record = self.get_object()
        serializer = self.get_serializer(record, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['GET'], detail=False, url_path='get_unclassified_records')
    def get_unclassified_records(self, request, pk=None):
        """Retrieve all records where status is unclassified"""
        records = ImageRecord.objects.filter(is_classified = False)

        serializer = serializers.UnclassifiedRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=True, url_path='send_classification')
    def send_classification(self, request, pk=None):
        """Update classification of record: update is_hotspot and upload painted image"""
        record = self.get_object()
        if record.is_classified:
            return Response(f"record {record.id} already classified", status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['is_classified'] = True

        serializer = self.get_serializer(record, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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