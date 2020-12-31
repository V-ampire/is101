from django.urls import path, include

from rest_framework_nested import routers

from api.v1.companies.views import CompanyViewSet
from api.v1.branches.views import BranchesViewSet


root_router = routers.SimpleRouter()
root_router.register('', CompanyViewSet, basename='company')


branches_router = routers.NestedSimpleRouter(root_router, r'', lookup='company')
branches_router.register(r'branches', BranchesViewSet, basename='company-branches')


urls = [
    path('', include(root_router.urls)),
    path('', include(branches_router.urls)),
]