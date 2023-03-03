"""
Database models
"""

import uuid
import os
from django.db import models
from django.conf import settings

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    # stripping extension of filename
    ext = os.path.splitext(filename)[1]
    # replacing filename with unique identifier
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads','image_records',filename)

class Location(models.Model):
    """Location of datapoint"""
    lat = models.FloatField()
    lon = models.FloatField()
    path = models.ForeignKey('Path',on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.lat},{self.lon})"

class ImageRecord(models.Model):
    class Status(models.TextChoices):
        Viewed = "Viewed"
        Visited = "Visited"
        Dismissed = "Dismissed"
        NotViewed = "Not viewed"

    """Image record taken by drone"""
    location = models.ForeignKey('Location',on_delete=models.CASCADE)
    date = models.DateTimeField()
    image_ir = models.ImageField(null=True, upload_to=recipe_image_file_path)
    image_rgb = models.ImageField(null=True, upload_to=recipe_image_file_path)
    image_masked = models.ImageField(null=True, blank=True, upload_to=recipe_image_file_path)
    is_hotspot = models.BooleanField(default=False)
    is_classified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NotViewed)

    def __str__(self):
        return f'id: {self.id}'
    
class Path(models.Model):
    """Path that drone took to collect data"""
    name = models.TextField(max_length=30)

    def __str__(self):
        return f"({self.id}) {self.name}"