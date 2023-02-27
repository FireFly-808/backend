"""
Django admin
"""

from django.contrib import admin
from core import models

admin.site.register(models.ImageRecord)
admin.site.register(models.Location)
