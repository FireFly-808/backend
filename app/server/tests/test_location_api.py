"""
Tests for locations api
"""

import os
import tempfile
from PIL import Image

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    ImageRecord,
    Location,
    Path,
)

from server.serializers import (
    ImageRecordSerializer,
    LocationSerializer,
)


LOCATION_URL = reverse('server:location-list')
GET_LOCS_BY_PATH_URL = reverse('server:get_locations_data_by_path')

class PublicAPITests(TestCase):
    """Test all location actions"""

    def setUp(self):
        self.client = APIClient()

    def test_get_locations(self):
        """Test retrieving locations"""
        path = Path.objects.create(name="toronto")
        Location.objects.create(x=1.1,y=2.2,path=path)
        Location.objects.create(x=3.3,y=4.4,path=path)
        
        res = self.client.get(LOCATION_URL)

        locs = Location.objects.all()
        serializer = LocationSerializer(locs,many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)