from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from hr import views
from biko_hr.views import home

from candidate import views

urlpatterns = [
    # path('', home),
    path('candidate_pool', views.get_candidate_pool, name="candidate_pool_dashboard"),
]

