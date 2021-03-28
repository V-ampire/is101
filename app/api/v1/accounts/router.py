from django.urls import path, include

from rest_framework.routers import SimpleRouter

from api.v1.accounts import views

root_router = SimpleRouter()
root_router.register(
    r'companies', views.CompanyAccountsViewSet, basename='account-companies'
)
root_router.register(
    r'employees', views.EmployeeAccountsViewSet, basename='account-employees'
)
root_router.register(
    r'admins', views.AdminAccountViewSet, basename='account-admins'
)

urls = [
    path('', include(root_router.urls)),
]