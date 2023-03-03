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
    Path,
)

from server.serializers import (
    ImageRecordSerializer,
    LocationSerializer,
    PathSerializer,
)

def update_status_url(record_id):
    return reverse('server:imagerecord-update-status', args=[record_id])

def send_classification_url(record_id):
    return reverse('server:imagerecord-send-classification', args=[record_id])

def create_record_no_image(location, date='2000-02-14T18:00:00Z'):
    """Create sample record with location"""
    return ImageRecord.objects.create(
        location=location,
        date=date,
    )

def create_record_custom(client, path = -10, lon=1.1, lat=2.2, date='2000-02-14T18:00:00Z'):
    """Create sample record with manual coordinates"""
    if path == -10:
        path = Path.objects.create(name="Vancouver")
    with tempfile.NamedTemporaryFile(suffix='.png') as image_file_ir:
        with tempfile.NamedTemporaryFile(suffix='.png') as image_file_rgb:
            img_ir = Image.new('RGB',(10,10))
            img_rgb = Image.new('RGB',(10,10))
            img_ir.save(image_file_ir, format='PNG')
            img_rgb.save(image_file_rgb, format='PNG')
            image_file_ir.seek(0)
            image_file_rgb.seek(0)
            payload = {
                "lon": lon,
                "lat": lat,
                "path_id": path.id,
                "date": date,
                "image_ir": image_file_ir,
                "image_rgb": image_file_rgb
            }
            res = client.post(ADD_RECORD_URL, payload, format='multipart')
            assert res.status_code == status.HTTP_201_CREATED
            record = ImageRecord.objects.get(id=res.data['id'])
            return record

ADD_RECORD_URL = reverse('server:add_record')
GET_LOCS_BY_PATH_URL = reverse('server:get_locations_data_by_path')
GET_UNCLASSIFIED_RECORDS_URL = reverse('server:imagerecord-get-unclassified-records')

LOCATION_URL = reverse('server:location-list')
IMAGERECORD_URL = reverse('server:imagerecord-list')
PATH_URL = reverse('server:path-list')

class PublicAPITests(TestCase):
    """Test all record actions"""

    def setUp(self):
        self.client = APIClient()
    
    def test_record_upload_custom(self):
        """Test creating an new record using apiview"""
        record = create_record_custom(self.client)

    def test_get_records(self):
        """Test retrieving records"""
        record1 = create_record_custom(self.client)
        record2 = create_record_custom(self.client, lon=123.435)

        res = self.client.get(IMAGERECORD_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_records_by_path(self):
        """Test retrieving records by path"""
        path1 = Path.objects.create(name='sanfran')
        path2 = Path.objects.create(name='los angeles')
        rec1 = create_record_custom(self.client, path=path1, date='2001-02-14T18:00:00Z')
        rec2 = create_record_custom(self.client, path=path1, lon=5.3, date='2026-02-14T18:00:00Z')
        rec3 = create_record_custom(self.client, path=path2)

        params = {'path_id':path1.id}
        res = self.client.get(GET_LOCS_BY_PATH_URL, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),2)

    def test_update_status(self):
        """Test updating the status of a record"""
        record = create_record_custom(self.client)
        loc = Location.objects.all()[0]
        self.assertEqual(record.location.id, loc.id)
        url = update_status_url(record.id)

        # change status to 'Dismissed'
        new_status = 'Dismissed'
        payload = {
            'status':new_status
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.status,new_status)

        # change status to 'Not viewed'
        new_status = 'Not viewed'
        payload = {
            'status':new_status
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.status,new_status)

    def test_update_invalid_status(self):
        """Test updating the status of a record with an invalid entry"""
        record = create_record_custom(self.client)
        old_status = record.status
        new_status = 'invalid status'
        payload = {
            'status':new_status
        }
        url = update_status_url(record.id)
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        record.refresh_from_db()
        self.assertEqual(record.status,old_status)

    def test_get_unclassified_records(self):
        """Test retrieving all unclassified records"""
        record1 = create_record_custom(self.client, lon=1.0)
        record2 = create_record_custom(self.client, lon=2.0)
        record3 = create_record_custom(self.client, lon=3.0)
        
        record2.is_classified = True
        record2.save()

        valid = {record1.id, record3.id}

        res = self.client.get(GET_UNCLASSIFIED_RECORDS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for rec in res.data:
            self.assertIn(rec['id'], valid)
            self.assertNotEqual(rec['id'], record2.id)

    def test_sending_classification(self):
        """Test sending classification of record"""
        record = create_record_custom(self.client, lon=1.0)
        self.assertEqual(record.is_classified, False)
        old_is_hotspot = record.is_hotspot

        with tempfile.NamedTemporaryFile(suffix='.png') as image_file_masked:
            img = Image.new('RGB',(10,10))
            img.save(image_file_masked, format='PNG')
            image_file_masked.seek(0)
            payload = {
                'is_hotspot' : True,
                'image_masked':image_file_masked
            }
            url = send_classification_url(record.id)
            res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertNotEqual(old_is_hotspot, record.is_hotspot)
        self.assertEqual(record.is_classified, True)

    def test_adding_new_path(self):
        """Test adding a new path"""
        cityname = "Toronto"
        payload = {'name':cityname}
        res = self.client.post(PATH_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        path = Path.objects.get(name=cityname)
        self.assertEqual(path.name,cityname)

    def test_get_all_paths(self):
        """Test retrieving all paths"""

        p1 = Path.objects.create(name="one")
        p2 = Path.objects.create(name="two")
        p3 = Path.objects.create(name="three")
        p4 = Path.objects.create(name="four")

        res = self.client.get(PATH_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
            




        

            

        


