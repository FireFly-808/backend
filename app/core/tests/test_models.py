"""
Tests for models
"""

from unittest.mock import patch

from django.test import TestCase

from core import models

class ModelTests(TestCase):
    """Test models"""

    def test_create_location(self):
        """Test creation of a location"""
        x = 123.123
        y = 456.456
        newLoc = models.Location.objects.create(
            x = x,
            y = y
        )
        self.assertEqual(str(newLoc),f"({x},{y})")

    def test_create_hotspot(self):
        """Test creation of a hotspot"""
        location = models.Location.objects.create(x = 1.1, y = 2.2)
        hotspot = models.Hotspot.objects.create(
            location = location,
            size = 3,
            status = 'hella bad'
        )
        self.assertEqual(str(hotspot),f'size:3')