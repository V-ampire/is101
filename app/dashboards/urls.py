from django.urls import path, re_path

from dashboards import views


app_name = 'dashboards'
urlpatterns = [
    # re_path(r'^admin/$|[\w\/]+', views.AdminDashboardView.as_view(), name='admin'),
    # re_path(r'^company/$|[\w\/]+', views.CompanyDashboardView.as_view(), name='company'),
    # re_path(r'^employee/$|[\w\/]+', views.EmployeeDashboardView.as_view(), name='employee'),
    path('admin/', views.CompanyDashboardView.as_view(), name='admin'),
    path('admin/<str:nested>/', views.CompanyDashboardView.as_view(), name='admin_nested'),
    path('company/', views.CompanyDashboardView.as_view(), name='company'),
    path('company/<str:nested>/', views.CompanyDashboardView.as_view(), name='company_nested')
]