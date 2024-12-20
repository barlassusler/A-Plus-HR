from django.urls import path
from .views import create_task_request, task_request_list, task_request_detail

urlpatterns = [
    path('', task_request_list, name='task_request_list'),
    path('task-request/', create_task_request, name='create_task_request'),
    path('<int:pk>/', task_request_detail, name='task_request_detail'),  # Detay sayfası

]
