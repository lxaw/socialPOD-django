# Generated by Django 3.2.9 on 2021-12-08 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_url_notification_url_arguments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='url_arguments',
            new_name='related_model_name',
        ),
        migrations.AddField(
            model_name='notification',
            name='related_id',
            field=models.IntegerField(null=True),
        ),
    ]
