# Generated by Django 5.1 on 2024-09-13 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0014_personalmessage_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalmessage',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]