from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from authentication import views
from biko_hr.views import home

urlpatterns = [
    path('', views.log_in),
    path('log-in/', views.log_in, name='log-in'),
    path('log-out/', views.log_out, name='log-out'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('user-dashboard/', login_required(home), name='user_dashboard'),
]

