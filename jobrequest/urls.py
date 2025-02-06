from django.urls import path
from .views import (
    create_task_request, 
    task_request_list, 
    task_request_detail,
    task_request_list_hr,
    task_request_list_org,
    accept_task_request, 
    assign_candidates,
    view_assigned_candidates
)

urlpatterns = [
    path('', task_request_list, name='task_request_list'),
    path('hr', task_request_list_hr, name='task_request_list_hr'),
    path('director', task_request_list_org, name='task_request_list_org'),
    path('task-request/', create_task_request, name='create_task_request'),
    path('<int:pk>/', task_request_detail, name='task_request_detail'),  # Detay sayfası
    path('jobrequest/<int:pk>/accept/', accept_task_request, name='accept_task_request'),
    path('jobrequest/<int:job_request_id>/assign/', assign_candidates, name='assign_candidates'),
    path('jobrequest/<int:job_request_id>/candidates/', view_assigned_candidates, name='view_assigned_candidates'),
]
