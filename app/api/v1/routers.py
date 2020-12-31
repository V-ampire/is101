from django.urls import path, include

from rest_framework_nested import routers

from api.v1.accounts import views as accounts_views
from api.v1.companies import views as companies_views
from api.v1.branches import views as branches_views


# Роутер для ресурса /accounts
accounts_router = routers.SimpleRouter()

accounts_router.register(
    r'companies', 
    accounts_views.CompanyAccountsViewSet, 
    basename='account-companies'
)


# Роутер для ресурса /accounts/companies/branches
companies_router = routers.NestedSimpleRouter(
    accounts_router, 
    r'companies', 
    lookup='company'
)
companies_router.register(
    r'branches', branches_views.BranchesViewSet, basename='company-branches'
)


accounts_urls = [
    path('', include(accounts_router.urls)),
    path('', include(companies_router.urls))
]