from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_application_list, name='job_application_list'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('new/', views.job_application_form, name='job_application_form'),
]

