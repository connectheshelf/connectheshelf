# Generated by Django 3.1.4 on 2020-12-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempReader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12)),
                ('otp', models.IntegerField(default=0)),
                ('status', models.CharField(default='pending', max_length=10)),
            ],
        ),
    ]
