# Generated by Django 5.0.2 on 2024-07-29 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0008_feedetails_discount1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedetails',
            name='Date',
        ),
        migrations.RemoveField(
            model_name='feedetails',
            name='Discount',
        ),
    ]
