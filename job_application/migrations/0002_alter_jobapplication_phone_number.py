# Generated by Django 5.1.4 on 2024-12-15 17:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Telefon numarası geçerli bir formatta olmalıdır.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]