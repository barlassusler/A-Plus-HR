# Generated by Django 5.1.4 on 2024-12-15 13:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('full_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Telefon numarası geçerli bir formatta olmalıdır.', regex='^\\+?1?\\d{9,15}$')])),
                ('residence_city', models.CharField(max_length=100)),
                ('residence_district', models.CharField(max_length=100)),
                ('education_level', models.CharField(choices=[('read_write', 'Okuma Yazma Belgesi'), ('primary', 'İlkokul'), ('middle', 'Ortaokul'), ('high', 'Lise'), ('university', 'Üniversite'), ('postgraduate', 'Yüksek Lisans ve Üzeri')], max_length=20)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('department_name', models.CharField(blank=True, max_length=255, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('desired_locations', models.ManyToManyField(related_name='applications', to='job_application.location')),
                ('applied_positions', models.ManyToManyField(related_name='applications', to='job_application.position')),
            ],
        ),
    ]