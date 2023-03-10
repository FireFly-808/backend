"""
Url mappings for the recipe app
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from server import views

router = DefaultRouter()

router.register('records', views.ImageRecordViewSet)
router.register('locations', views.LocationViewSet)
router.register('paths', views.PathViewSet)

app_name = 'server'

urlpatterns = [ 
    path('',include(router.urls)),
    path('add_record/', views.add_record, name='add_record'),
    path('get_locations_data_by_path/', views.get_locations_data_by_path, name='get_locations_data_by_path'),
]