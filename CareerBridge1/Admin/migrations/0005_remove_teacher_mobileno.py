# Generated by Django 5.0.2 on 2024-07-17 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='MobileNo',
        ),
    ]
