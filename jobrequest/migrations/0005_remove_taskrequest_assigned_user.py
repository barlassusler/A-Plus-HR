# Generated by Django 5.0.4 on 2024-12-15 14:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("jobrequest", "0004_taskrequest_description_taskrequest_education_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskrequest",
            name="assigned_user",
        ),
    ]