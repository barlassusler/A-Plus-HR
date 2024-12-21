from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from organization import views

urlpatterns = [
    path('', views.dashboard, name="organization_dashboard"),
    path('profile/', views.get_profile, name='organization_profile'),
]

