from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from hr import views
from biko_hr.views import home

urlpatterns = [
    path('', views.dashboard, name="hr_dashboard"),
    path('profile', views.get_profile, name="hr_profile"),
    path('my-interviews/', views.my_interviews, name='my_interviews'),
    path('interview/<int:interview_id>/assess/', views.interview_assessment, name='interview_assessment'),
]

