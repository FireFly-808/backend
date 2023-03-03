"""
Tests for models
"""

from unittest.mock import patch

from django.test import TestCase

from core import models

import os
import tempfile
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


ADD_RECORD_URL = reverse('server:add_record')

class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        client = APIClient()

    def test_create_location(self):
        """Test creation of a location"""
        lon = 123.123
        lat = 456.456
        path = models.Path.objects.create(name='toronto')
        newLoc = models.Location.objects.create(
            lat = lat,
            lon = lon,
            path = path
        )
        self.assertEqual(newLoc.lon,lon)