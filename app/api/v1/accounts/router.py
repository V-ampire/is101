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

urls = [
    path('', include(root_router.urls)),
    path('no_profiles', views.UsersWithNoProfileView.as_view(), name='accounts-no_profiles'),
    path(
        'no_profiles/count/', 
        views.UsersWithNoProfileCountView.as_view(), 
        name='accounts-no_profiles-count'
    ),
]