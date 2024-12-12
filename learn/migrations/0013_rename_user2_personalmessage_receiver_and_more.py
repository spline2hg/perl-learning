# Generated by Django 5.1 on 2024-09-13 17:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0012_personalmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalmessage',
            old_name='user2',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='personalmessage',
            old_name='user1',
            new_name='sender',
        ),
        migrations.AddField(
            model_name='personalmessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
