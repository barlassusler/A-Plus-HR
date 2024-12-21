from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from hr import views
from biko_hr.views import home

urlpatterns = [
    path('', home),
    path('profile', views.get_profile, name="hr_profile"),
]

