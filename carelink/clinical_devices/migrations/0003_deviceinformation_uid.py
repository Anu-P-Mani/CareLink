# Generated by Django 5.0.2 on 2024-03-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_devices', '0002_alter_deviceinformation_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceinformation',
            name='uid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
