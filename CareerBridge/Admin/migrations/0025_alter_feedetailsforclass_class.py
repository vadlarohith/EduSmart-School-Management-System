# Generated by Django 5.0.2 on 2024-07-29 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0024_remove_feedetailsforclass_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedetailsforclass',
            name='Class',
            field=models.CharField(max_length=10),
        ),
    ]
