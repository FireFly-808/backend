"""
Database models
"""

import uuid
import os
from django.db import models
from django.conf import settings

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    name = os.path.basename(filename)
    # stripping extension of filename
    ext = os.path.splitext(filename)[1]
    # replacing filename with unique identifier
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'ir', filename)

    # folder = 'ir'
    # if rgb:
    #     folder = 'rgb'

    # return os.path.join('uploads', folder, filename)
        

class Location(models.Model):
    """Location of datapoint"""
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"({self.x},{self.y})"

class ImageRecord(models.Model):
    """Image record taken by drone"""
    location = models.ForeignKey('Location',on_delete=models.CASCADE)
    date = models.DateTimeField()
    ir_image = models.ImageField(null=False, upload_to=recipe_image_file_path)
    rgb_image = models.ImageField(null=False, upload_to=recipe_image_file_path)

    def __str__(self):
        return f'date:{self.date}'

class Hotspot(models.Model):
    """Hotspot determined by the classification script"""
    location = models.ForeignKey('Location',on_delete=models.CASCADE)
    size = models.IntegerField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f'size:{self.size}'
