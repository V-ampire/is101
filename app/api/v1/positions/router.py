from rest_framework import routers

from api.v1.positions.views import PositionViewSet


router = routers.SimpleRouter()

router.register('', PositionViewSet)