from rest_framework import routers

from api.v1.employees.views import EmployeeViewSet


router = routers.SimpleRouter()

router.register('', EmployeeViewSet)