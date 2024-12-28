from django.db import models
from biko_hr.models import Location, Organization, IncubationJob, Position

class JobRequest(models.Model): #talep eğer kabul edilirse IncubationJob tablosuna eklenilecek.
    TASK_TYPE_CHOICES = [
        ('Mevcut Kadro', 'Mevcut Kadro'),
        ('İlave Kadro', 'İlave Kadro'),
    ]
    WORK_TYPE_CHOICES = [
        ('Tam Zamanlı', 'Tam Zamanlı'),
        ('Yarı Zamanlı', 'Yarı Zamanlı'),
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE,blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,blank=True, null=True)

    position_type= models.CharField(max_length=100, choices=TASK_TYPE_CHOICES,blank=True, null=True)
    position_name = models.ForeignKey(Position,on_delete=models.CASCADE,blank=True, null=True)
    new_position_name = models.CharField(max_length=100, blank=True, null=True)
    replacement_for = models.CharField(max_length=100, blank=True, null=True)  # Kimin Yerine
    # task_name = models.ForeignKey(IncubationJob, on_delete=models.SET_NULL, null=True, blank=True)  # Görev Adı Dropdown
    # new_task_name = models.CharField(max_length=100, blank=True, null=True)  # Yeni Görev Adı
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    request_reason = models.TextField(blank=True, null=True)  # Talep Nedeni
    description = models.TextField(blank=True, null=True)  # Açıklama
    desired_start_date = models.DateField(blank=True, null=True)  # Göreve Başlama Tarihi
    desired_personnel_count = models.PositiveIntegerField()  # Alınacak Kişi Sayısı
    desired_experience_years = models.PositiveIntegerField(blank=True, null=True)  # Deneyim Yılı
    required_education_level = models.CharField(max_length=255, blank=True, null=True)  # Eğitim
    special_requirements = models.TextField(blank=True, null=True)  # Özel Nitelikler
    created_at = models.DateTimeField(auto_now_add=True)
    request_status_hr = models.CharField(max_length=50, default="Pending", blank=True)
    request_status_organization_manager = models.CharField(max_length=50, default="Pending", blank=True)


