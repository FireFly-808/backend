"""
Tests for records api
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
def create_record_no_image(location, date='2000-02-14T18:00:00Z'):
    """Create sample record with location"""
    return ImageRecord.objects.create(
        location=location,
        date=date,
    )

def create_record_custom(client, path_id = 3, x=1.1, y=2.2, date='2000-02-14T18:00:00Z'):
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
                "x_coord": x,
                "y_coord": y,
                "path_id": path_id,
                "date": date,
                "image_ir": image_file_ir,
                "image_rgb": image_file_rgb
            }
            res = client.post(ADD_RECORD_URL, payload, format='multipart')
            return res

ADD_RECORD_URL = reverse('server:add_record')
GET_LOCS_BY_PATH_URL = reverse('server:get_locations_data_by_path')


LOCATION_URL = reverse('server:location-list')
IMAGERECORD_URL = reverse('server:imagerecord-list')
HOTSPOT_URL = reverse('server:hotspot-list')

class PublicAPITests(TestCase):
    """Test all record actions"""

    def setUp(self):
        self.client = APIClient()
    
    def test_record_upload_custom(self):
        """Test creating an new record using apiview"""
        res = create_record_custom(self.client, path_id =4)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image_ir', res.data)
        self.assertIn('image_rgb', res.data)

    def test_get_records(self):
        """Test retrieving records"""
        res = create_record_custom(self.client)
        
        res = self.client.get(IMAGERECORD_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # print(res.data)

        recs = ImageRecord.objects.all()
        serializer = ImageRecordSerializer(recs,many=True)
        # print(serializer.data)
        # self.assertEqual(res.data, serializer.data)

    def test_get_records_by_path(self):
        """Test retrieving records by path"""
        res1 = create_record_custom(self.client, path_id=4, date='2001-02-14T18:00:00Z')
        res2 = create_record_custom(self.client, path_id=4, x=5.3, date='2026-02-14T18:00:00Z')
        res3 = create_record_custom(self.client, path_id=2)


        record = ImageRecord.objects.get(id=res2.data['id'])
        hotspot = Hotspot.objects.create(
            record = record,
            size = 654,
            status = 'hella poor'
        )

        params = {'path_id':4}
        res = self.client.get(GET_LOCS_BY_PATH_URL, params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # for loc_data in res.data:
        #     print(loc_data)
            
            

        


