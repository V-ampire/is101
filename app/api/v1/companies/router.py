from django.urls import path, include

from rest_framework_nested import routers

from api.v1.companies.views import CompanyViewSet
from api.v1.branches.views import BranchesViewSet
from api.v1.employees.views import EmployeeViewSet


root_router = routers.SimpleRouter()
root_router.register('', CompanyViewSet, basename='companies')


branches_router = routers.NestedSimpleRouter(root_router, r'', lookup='company')
branches_router.register(r'branches', BranchesViewSet, basename='company-branches')

employees_router = routers.NestedSimpleRouter(branches_router, r'branches', lookup='branch')
employees_router.register(r'employees', EmployeeViewSet, basename='company-branch-employees')


urls = [
    path('', include(root_router.urls)),
    path('', include(branches_router.urls)),
    path('', include(employees_router.urls)),
]

