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
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"({self.x},{self.y})"

class ImageRecord(models.Model):
    """Image record taken by drone"""
    type = models.CharField(max_length=10, null=True)
    location = models.ForeignKey('Location',on_delete=models.CASCADE)
    date = models.DateTimeField()
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return f'id: {self.id}'

class Hotspot(models.Model):
    """Hotspot determined by the classification script"""
    location = models.ForeignKey('Location',on_delete=models.CASCADE)
    size = models.IntegerField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f'size:{self.size}'
