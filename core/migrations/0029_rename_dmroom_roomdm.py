# Generated by Django 3.2.10 on 2022-01-17 15:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0028_dmroom'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DMRoom',
            new_name='RoomDm',
        ),
    ]