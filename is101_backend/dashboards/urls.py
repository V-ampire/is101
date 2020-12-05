from django.urls import path

from dashboards import views


app_name = 'dashboards'
urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin'),
]