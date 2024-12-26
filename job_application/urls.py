from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.job_application_list, name='job_application_list'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('new/', views.job_application_form, name='job_application_form'),
    path('success/', views.success_page, name='success_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)