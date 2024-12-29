from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="director_dashboard"),
    path('profile/', views.get_profile, name='director_profile'),
]

