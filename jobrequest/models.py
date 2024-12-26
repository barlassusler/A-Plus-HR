from django.db import models
from biko_hr.models import Location, Organization, Job, Position

class JobRequest(models.Model):
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
    position_type_2= models.CharField(max_length=100, choices=TASK_TYPE_CHOICES,blank=True, null=True)
    position_type = models.ForeignKey(Position,on_delete=models.CASCADE,blank=True, null=True)
    replacement_for = models.CharField(max_length=100, blank=True, null=True)  # Kimin Yerine
    task_name = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)  # Görev Adı Dropdown
    new_task_name = models.CharField(max_length=100, blank=True, null=True)  # Yeni Görev Adı
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    request_reason = models.TextField(blank=True, null=True)  # Talep Nedeni
    description = models.TextField(blank=True, null=True)  # Açıklama
    start_date = models.DateField(blank=True, null=True)  # Göreve Başlama Tarihi
    personnel_count = models.PositiveIntegerField()  # Alınacak Kişi Sayısı
    experience_years = models.PositiveIntegerField(blank=True, null=True)  # Deneyim Yılı
    education = models.CharField(max_length=255, blank=True, null=True)  # Eğitim
    special_requirements = models.TextField(blank=True, null=True)  # Özel Nitelikler
    created_at = models.DateTimeField(auto_now_add=True)


