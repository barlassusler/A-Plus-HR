# Generated by Django 4.2.4 on 2024-12-26 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biko_hr', '0003_profile_location_profile_organization_and_more'),
        ('jobrequest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='position_type_2',
            field=models.CharField(blank=True, choices=[('Mevcut Kadro', 'Mevcut Kadro'), ('İlave Kadro', 'İlave Kadro')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biko_hr.location'),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biko_hr.organization'),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='position_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biko_hr.position'),
        ),
    ]
