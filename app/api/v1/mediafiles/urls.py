from django.urls import path

from api.v1.mediafiles import views


urlpatterns = [
    path(
        'companies/<str:company_uuid>/company_media/<str:media_name>/', 
        views.CompanyMediaView.as_view(), 
        name='company_media'
    ),
    path(
        'companies/<str:company_uuid>/employees/<str:employee_uuid>/<str:media_name>/', 
        views.EmployeeMediaView.as_view(),
        name='employee_media'
    ),

]    
    