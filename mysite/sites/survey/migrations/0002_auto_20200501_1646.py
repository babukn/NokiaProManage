# Generated by Django 3.0.5 on 2020-05-01 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
