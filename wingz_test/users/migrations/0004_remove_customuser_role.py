# Generated by Django 4.2.13 on 2024-08-01 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
    ]