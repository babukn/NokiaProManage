# Generated by Django 3.0.5 on 2020-05-10 00:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('porjectmanage', '0004_auto_20200509_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='usernames', to=settings.AUTH_USER_MODEL),
        ),
    ]
