# Generated by Django 5.1 on 2024-09-06 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_alter_classroom_educator'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
