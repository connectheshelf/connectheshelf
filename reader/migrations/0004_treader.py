# Generated by Django 3.1.4 on 2020-12-22 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0003_delete_tempreader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12)),
                ('otp', models.CharField(default='000000', max_length=8)),
                ('status', models.CharField(default='pending', max_length=10)),
            ],
        ),
    ]