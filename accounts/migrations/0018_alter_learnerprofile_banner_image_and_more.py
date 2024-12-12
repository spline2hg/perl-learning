# Generated by Django 5.1 on 2024-09-19 22:12

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_educatorprofile_banner_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learnerprofile',
            name='banner_image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dzchm8yml/image/upload/v1726758796/cmlwhcdl4unrdcipflrv.webp', max_length=255, verbose_name='banner_image'),
        ),
        migrations.AlterField(
            model_name='learnerprofile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dzchm8yml/image/upload/v1726752664/yjavnsy8nu8xiqvqeeov.jpg', max_length=255, verbose_name='profile_image'),
        ),
    ]
