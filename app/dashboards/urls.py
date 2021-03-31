from django.urls import path, re_path

from dashboards import views


app_name = 'dashboards'
urlpatterns = [
    re_path(r'^admin/[\w\/]+', views.AdminDashboardView.as_view(), name='admin'),
    re_path(r'^company', views.CompanyDashboardView.as_view(), name='company'),
    re_path(r'^employee/[\w\/]+', views.EmployeeDashboardView.as_view(), name='employee'),
    #re_path('(?P<nested_url>[\w\/]+)', views.AdminDashboardView.as_view(), name='nested_urls'),
]