# Generated by Django 5.0.2 on 2024-07-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0012_student_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='Password',
            field=models.CharField(default='000', max_length=20),
            preserve_default=False,
        ),
    ]
