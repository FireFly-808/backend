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


def create_record_custom(client):
    """Create sample record with manual coordinates"""
    with tempfile.NamedTemporaryFile(suffix='.png') as image_file_ir:
        with tempfile.NamedTemporaryFile(suffix='.png') as image_file_rgb:
            img_ir = Image.new('RGB',(10,10))
            img_rgb = Image.new('RGB',(10,10))
            img_ir.save(image_file_ir, format='PNG')
            img_rgb.save(image_file_rgb, format='PNG')
            image_file_ir.seek(0)
            image_file_rgb.seek(0)
            payload = {
                "x_coord": 1.1,
                "y_coord": 2.2,
                "path_id": 3,                
                "date": "2023-02-14T18:00:00Z",
                "image_ir": image_file_ir,
                "image_rgb": image_file_rgb
            }
            res = client.post(ADD_RECORD_URL, payload, format='multipart')
            return res

class ModelTests(TestCase):
    """Test models"""

    def setUp(self):
        client = APIClient()

    def test_create_location(self):
        """Test creation of a location"""
        x = 123.123
        y = 456.456
        path_id = 1
        newLoc = models.Location.objects.create(
            x = x,
            y = y,
            path_id = path_id
        )
        self.assertEqual(newLoc.x,x)