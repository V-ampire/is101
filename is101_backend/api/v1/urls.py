from django.urls import path, include

from rest_framework import routers

from api.v1.companies.views import CompanyViewSet


app_name = 'api_v1'

router = routers.SimpleRouter()

router.register(r'companies', CompanyViewSet)

urlpatterns = router.urls
# urlpatterns = [
#     path('', include(router.urls))
# ]