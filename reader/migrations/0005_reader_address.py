# Generated by Django 3.1.4 on 2020-12-24 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0004_treader'),
    ]

    operations = [
        migrations.AddField(
            model_name='reader',
            name='address',
            field=models.TextField(default='Not provided'),
        ),
    ]
