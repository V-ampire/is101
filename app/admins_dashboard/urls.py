from django.urls import path

from admins_dashboard import views


app_name = 'admins_dashboard'
urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='main'),
]