# Generated by Django 5.0.2 on 2024-05-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autherization', '0017_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=10),
        ),
    ]
