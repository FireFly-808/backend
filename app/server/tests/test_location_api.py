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
    Hotspot
)

from server.serializers import (
    ImageRecordSerializer,
    LocationSerializer,
)


LOCATIONS_URL = reverse('server:location-list')

class PublicAPITests(TestCase):
    """Test all location actions"""

    def setUp(self):
        self.client = APIClient()

    def test_get_locations_by_path(self):
        """Test retrieving locations from a path"""
        loc1 = Location.objects.create(x=1.1,y=1.2,path=1)
        loc2 = Location.objects.create(x=2.1,y=2.2,path=1)
        loc3 = Location.objects.create(x=351.1,y=5341.2,path=2)

        payload = {'path_id':'1'}
        res = self.client.get(LOCATIONS_URL,payload)

        s1 = LocationSerializer(loc1)
        s2 = LocationSerializer(loc2)
        s3 = LocationSerializer(loc3)

        self.assertIn(s1.data,res.data)
        self.assertIn(s2.data,res.data)
        self.assertNotIn(s3.data,res.data)
