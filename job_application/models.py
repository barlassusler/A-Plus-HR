from django.db import models
from django.core.validators import RegexValidator


class JobApplication(models.Model):
    # Özgeçmiş Yükleme
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    # Kişisel Bilgiler
    full_name = models.CharField(max_length=255)  # Adı Soyadı
    birth_date = models.DateField()  # Doğum Tarihi
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon numarası geçerli bir formatta olmalıdır.")
        ]
    )  # Telefon Numarası
    residence_city = models.CharField(max_length=100)  # İkamet İl
    residence_district = models.CharField(max_length=100)  # İkamet İlçe

    # Başvurduğu Pozisyon
    applied_positions = models.ManyToManyField('Position', related_name='applications')  # Birden fazla seçenek

    # Eğitim Durumu
    EDUCATION_LEVELS = [
        ('read_write', 'Okuma Yazma Belgesi'),
        ('primary', 'İlkokul'),
        ('middle', 'Ortaokul'),
        ('high', 'Lise'),
        ('university', 'Üniversite'),
        ('postgraduate', 'Yüksek Lisans ve Üzeri'),
    ]
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    school_name = models.CharField(max_length=255, null=True, blank=True)  # Okul Adı (Zorunlu olabilir)
    department_name = models.CharField(max_length=255, null=True, blank=True)  # Bölüm Adı

    # Çalışmak İstediği Lokasyonlar
    desired_locations = models.ManyToManyField('Location', related_name='applications')

    # Anahtar Kelimeler
    keywords = models.TextField(null=True, blank=True)  # Filtreleme için kullanılacak

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Lise ve üstü için okul ve bölüm adı kontrolü
        if self.education_level in ['high', 'university', 'postgraduate']:
            if not self.school_name or not self.department_name:
                raise ValueError("Lise ve üstü eğitim için okul ve bölüm adı zorunludur.")
        super().save(*args, **kwargs)


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

