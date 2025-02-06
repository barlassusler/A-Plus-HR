from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from hr import views
from biko_hr.views import home

from candidate import views

urlpatterns = [
    # path('', home),
    path('candidate_pool/', views.get_candidate_pool, name='candidate_pool_dashboard'),

    path('candidate/<int:candidate_id>/profile/', views.candidate_profile, name='candidate_profile'),
    path('candidate/<int:application_id>/schedule-interview/', views.schedule_interview, name='schedule_interview'),
    path('candidate/<int:candidate_id>/assign-job/', views.assign_job, name='assign_job'),
    path('candidate/<int:candidate_id>/add-note/', views.add_hr_note, name='add_hr_note'),
    path('candidate/<int:candidate_id>/add-reference/', views.add_reference, name='add_reference'),

    path('category/<int:category_id>/detail/', views.category_detail, name='category_detail'),
    path('application/<int:application_id>/evaluate/', views.candidate_evaluation, name='candidate_evaluation'),
    path('incubation/<int:incubation_id>/evaluate/', views.incubation_evaluation, name='incubation_evaluation'),
]

