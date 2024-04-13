# Generated by Django 5.0.2 on 2024-03-12 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_devices', '0008_remove_deviceinformation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinical_devices.deviceinformation')),
            ],
        ),
    ]
