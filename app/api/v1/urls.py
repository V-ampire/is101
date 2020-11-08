from rest_framework import routers

from api.v1.companies.views import CompanyViewSet


router = routers.SimpleRouter()

router.register(r'companies', CompanyViewSet, basename='companies')


urlpatterns = router.urls