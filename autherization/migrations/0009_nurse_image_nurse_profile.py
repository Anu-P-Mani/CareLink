# Generated by Django 5.0.2 on 2024-03-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autherization', '0008_remove_nurse_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurse',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='nurse',
            name='profile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]