# Generated by Django 5.1 on 2024-09-19 21:44

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_educatorprofile_banner_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educatorprofile',
            name='banner_image',
            field=cloudinary.models.CloudinaryField(default='https://collection.cloudinary.com/dzchm8yml/506855558e535154d0c8d04684b6192c?', max_length=255, verbose_name='banner_image'),
        ),
        migrations.AlterField(
            model_name='educatorprofile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(default='https://collection.cloudinary.com/dzchm8yml/8a47dba2a9b3ce16cef5a9a58d02b433', max_length=255, verbose_name='profile_image'),
        ),
    ]
