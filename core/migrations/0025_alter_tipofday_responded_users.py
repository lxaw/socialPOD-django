# Generated by Django 3.2.9 on 2022-01-12 18:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0024_alter_tipofday_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipofday',
            name='responded_users',
            field=models.ManyToManyField(related_name='tip_set', to=settings.AUTH_USER_MODEL),
        ),
    ]