# Generated by Django 5.2 on 2025-04-16 07:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDrive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('point_of_contact', models.CharField(max_length=100)),
                ('year_of_passing', models.IntegerField()),
                ('job_received_date', models.DateField()),
                ('job_posted_date', models.DateField()),
                ('job_posted_by', models.CharField(max_length=100)),
                ('student_data_shared_date', models.DateField(blank=True, null=True)),
                ('interview_date', models.DateField(blank=True, null=True)),
                ('interview_posted_date', models.DateField(blank=True, null=True)),
                ('results_declaration_status', models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('IN_PROCESS', 'In Process'), ('PENDING', 'Pending'), ('DECLARED', 'Declared')], default='NOT_STARTED', max_length=20)),
                ('results_declaration_date', models.DateField(blank=True, null=True)),
                ('no_of_selects', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_drives', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_drives', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
