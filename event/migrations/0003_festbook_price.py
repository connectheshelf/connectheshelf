# Generated by Django 3.1.4 on 2020-12-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_festorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='festbook',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]