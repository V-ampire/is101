from django.urls import path, re_path

from dashboards import views


app_name = 'dashboards'
urlpatterns = [
    re_path('', views.AdminDashboardView.as_view(), name='admin'),
    #re_path('(?P<nested_url>[\w\/]+)', views.AdminDashboardView.as_view(), name='nested_urls'),
]