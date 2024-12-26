from django.db import models
from django.core.validators import RegexValidator

class Candidate(models.Model):
    full_name = models.CharField(max_length=55)  # Adı Soyadı
    birth_date = models.DateField()  # Doğum Tarihi
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon numarası geçerli bir formatta olmalıdır.")]
    )  # Telefon Numarası
    residence_city = models.CharField(max_length=100)  # İkamet İl
    residence_district = models.CharField(max_length=100)  # İkamet İlçe
    education_level = models.CharField(
        max_length=20,
        choices=[
            ('read_write', 'Okuma Yazma Belgesi'),
            ('primary', 'İlkokul'),
            ('middle', 'Ortaokul'),
            ('high', 'Lise'),
            ('university', 'Üniversite'),
            ('postgraduate', 'Yüksek Lisans ve Üzeri'),
        ]
    )
    school_name = models.CharField(max_length=55, null=True, blank=True)  # Okul Adı
    department_name = models.CharField(max_length=75, null=True, blank=True)  # Bölüm Adı

    def __str__(self):
        return self.full_name

class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')  # Aday ile ilişki
    applied_positions = models.ManyToManyField('Position', related_name='applications')  # Pozisyonlar
    desired_locations = models.ManyToManyField('Location', related_name='applications')  # Lokasyonlar
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Özgeçmiş Yükleme
    application_date = models.DateTimeField(auto_now_add=True)  # Başvuru Tarihi

    def __str__(self):
        return f"Application by {self.candidate.full_name} on {self.application_date}"

class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name
