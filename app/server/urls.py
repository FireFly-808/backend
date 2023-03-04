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
router.register('paths', views.PathViewSet)

app_name = 'server'

urlpatterns = [ 
    path('',include(router.urls)),
    path('add_record/', views.add_record, name='add_record'),
    path('add_record_from_drone/', views.add_record_from_drone, name='add_record_from_drone'),
    # path('get_distinct_path_ids/', views.get_distinct_path_ids, name='get_distinct_path_ids'),
    path('get_locations_data_by_path/', views.get_locations_data_by_path, name='get_locations_data_by_path'),
]