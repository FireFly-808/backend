"""
Tests for actions with images
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

from record.serializers import (
    ImageRecordSerializer
)

def create_record(**params):
    """Create and return a sample image record"""
    loc = Location.objects.create(x=1.0,y=2.0)

    with tempfile.NamedTemporaryFile(suffix='.png') as image_file:
        img = Image.new('RGB',(10,10))
        img.save(image_file, format='PNG')
        image_file.seek(0)
        data = {
            "type": "rgb",
            "location": loc.id,
            "date": "2023-02-14T18:00:00Z",
            "image": image_file
        }
        record = ImageRecord.objects.create(**data)
        return record

ADD_RECORD_URL = reverse('record:image_record_view')

class PublicAPITests(TestCase):
    """Test all record actions"""

    def setUp(self):
        self.client = APIClient()

    def test_record_upload(self):
        """Test creating an new record"""
        with tempfile.NamedTemporaryFile(suffix='.png') as image_file:
            img = Image.new('RGB',(10,10))
            img.save(image_file, format='PNG')
            image_file.seek(0)
            payload = {
                "type": "rgb",
                "x_coord": 123.123,
                "y_coord": 456.456,
                "date": "2023-02-14T18:00:00Z",
                "image": image_file
            }
            res = self.client.post(ADD_RECORD_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)



