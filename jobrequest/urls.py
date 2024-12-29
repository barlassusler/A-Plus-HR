from django.urls import path
from .views import create_task_request, task_request_list, task_request_detail,task_request_list_hr,task_request_list_org,accept_task_request

urlpatterns = [
    path('', task_request_list, name='task_request_list'),
    path('hr', task_request_list_hr, name='task_request_list_hr'),
    path('director', task_request_list_org, name='task_request_list_org'),
    path('task-request/', create_task_request, name='create_task_request'),
    path('<int:pk>/', task_request_detail, name='task_request_detail'),  # Detay sayfası
    path('jobrequest/<int:pk>/accept/', accept_task_request, name='accept_task_request'),

]
