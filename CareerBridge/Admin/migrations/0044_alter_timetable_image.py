# Generated by Django 5.0.2 on 2024-08-27 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0043_teachertimetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='Image',
            field=models.ImageField(null=True, upload_to='image/'),
        ),
    ]
