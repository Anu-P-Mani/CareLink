# Generated by Django 5.0.2 on 2024-03-07 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinformation',
            name='product_image',
            field=models.FileField(upload_to='images/'),
        ),
    ]
