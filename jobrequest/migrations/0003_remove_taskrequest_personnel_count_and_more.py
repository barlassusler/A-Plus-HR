# Generated by Django 5.0.4 on 2024-12-15 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "jobrequest",
            "0002_taskrequest_personnel_count_taskrequest_start_date_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskrequest",
            name="personnel_count",
        ),
        migrations.RemoveField(
            model_name="taskrequest",
            name="start_date",
        ),
        migrations.RemoveField(
            model_name="taskrequest",
            name="work_type",
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="jobrequest.location"
            ),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="jobrequest.organization",
            ),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="task_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="jobrequest.task",
            ),
        ),
        migrations.AlterField(
            model_name="taskrequest",
            name="task_type",
            field=models.CharField(
                choices=[
                    ("Yeni Görev", "Yeni Görev"),
                    ("Mevcut Kadro", "Mevcut Kadro"),
                    ("İlave Kadro", "İlave Kadro"),
                ],
                max_length=50,
            ),
        ),
    ]