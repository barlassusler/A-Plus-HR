# Generated by Django 5.0.4 on 2024-12-15 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobrequest", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="taskrequest",
            name="personnel_count",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="taskrequest",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="taskrequest",
            name="work_type",
            field=models.CharField(
                choices=[
                    ("Tam Zamanlı", "Tam Zamanlı"),
                    ("Yarı Zamanlı", "Yarı Zamanlı"),
                ],
                default="Tam Zamanlı",
                max_length=50,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="assigned_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="location",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="organization",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="task_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="task_type",
            field=models.CharField(
                choices=[
                    ("Mevcut Kadro", "Mevcut Kadro"),
                    ("İlave Kadro", "İlave Kadro"),
                ],
                max_length=50,
            ),
        ),
    ]