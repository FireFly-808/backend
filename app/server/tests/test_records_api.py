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

from server import serializers

def create_record(location, type='rgb', date='2000-02-14T18:00:00Z'):
    """Create sample record with location"""
    return ImageRecord.objects.create(
        type=type,
        location=location,
        date=date,
    )

def create_record_manual(client, type):
    """Create sample record with manual coordinates"""
    with tempfile.NamedTemporaryFile(suffix='.png') as image_file:
        img = Image.new('RGB',(10,10))
        img.save(image_file, format='PNG')
        image_file.seek(0)
        payload = {
            "type": type,
            "x_coord": 123.123,
            "y_coord": 456.456,
            "date": "2023-02-14T18:00:00Z",
            "image": image_file
        }
        res = client.post(ADD_RECORD_URL, payload, format='multipart')
        return res

ADD_RECORD_URL = reverse('server:image_record_view')

class PublicAPITests(TestCase):
    """Test all record actions"""

    def setUp(self):
        self.client = APIClient()

    def test_record_upload_custom(self):
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

    
    def test_record_upload_default(self):
        """Test creating an new record using viewset override"""
        loc = Location.objects.create(x=1.1,y=2.2)

        url = reverse('server:imagerecord-add-custom-record')
        with tempfile.NamedTemporaryFile(suffix='.png') as image_file:
            img = Image.new('RGB',(10,10))
            img.save(image_file, format='PNG')
            image_file.seek(0)
            payload = {
                "type": "rgb",
                "x_coord": 1.1,
                "y_coord": 2.2,
                "date": "2023-02-14T18:00:00Z",
                "image": image_file
            }
            res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)
        recs = ImageRecord.objects.all()
        serializer = serializers.ImageRecordSerializer(recs,many=True)
        # check that a location with the same coordinates was not created
        self.assertEqual(loc.id,serializer.data[0]['location'])


    def test_get_locations(self):
        """Test retrieving locations"""
        Location.objects.create(x=1.1,y=2.2)
        Location.objects.create(x=3.3,y=4.4)
        url = reverse('server:location-list')
        res = self.client.get(url)

        locs = Location.objects.all()
        serializer = serializers.LocationSerializer(locs,many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_records(self):
        """Test retrieving records"""
        res = create_record_manual(self.client, 'rgb')
        res = create_record_manual(self.client, 'ir')
        
        url = reverse('server:imagerecord-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # print(res.data)

        recs = ImageRecord.objects.all()
        serializer = serializers.ImageRecordSerializer(recs,many=True)
        # print(serializer.data)

        # self.assertEqual(res.data, serializer.data)

    def test_get_record_pair_by_loc_id(self):
        """Test retrieving a pair of records based on location id"""
        loc = Location.objects.create(x=1.1,y=2.2)
        rgb1 = create_record(loc, type='rgb', date='2020-02-14T18:00:00Z')
        ir1 = create_record(loc, type='ir', date='2020-02-14T18:00:00Z')
        rgb2 = create_record(loc, type='rgb', date='2021-02-14T18:00:00Z')
        ir2 = create_record(loc, type='ir', date='2021-02-14T18:00:00Z')

        url = reverse('server:imagerecord-get-record-pair')
        params = {'loc_id':f'{loc.id}'}
        res = self.client.get(url,params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)



