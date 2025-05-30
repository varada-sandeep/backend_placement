# Generated by Django 5.2 on 2025-04-16 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drives', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydrive',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_drives', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='companydrive',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_drives', to=settings.AUTH_USER_MODEL),
        ),
    ]
