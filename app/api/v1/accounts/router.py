from django.urls import path, include

from rest_framework.routers import SimpleRouter

from api.v1.accounts import views

root_router = SimpleRouter()
root_router.register(
    r'companies', 
    views.CompanyAccountsViewSet, 
    basename='account-companies'
)

urls = [
    path('', include(root_router.urls)),
]