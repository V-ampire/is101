from django.urls import path, include

from rest_framework import routers

from api.v1.positions.views import PositionViewSet


root_router = routers.SimpleRouter()

root_router.register('', PositionViewSet, basename='position')

urls = [
    path('', include(root_router.urls)),
]