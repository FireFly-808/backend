"""
Url mappings for the recipe app
"""

from django.urls import (
    path,
    include,
)
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from server import views

router = DefaultRouter()

router.register('records', views.ImageRecordViewSet)
router.register('locations', views.LocationViewSet)
router.register('hotspots', views.HotspotViewSet)

app_name = 'server'

urlpatterns = [ 
    path('',include(router.urls)),
    url(r'^add_record/',views.ImageRecordApiView.as_view(), name='image_record_view')
] 