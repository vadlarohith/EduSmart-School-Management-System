# Generated by Django 5.0.2 on 2024-08-17 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0039_alter_exammarks_marks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examtype',
            old_name='Access',
            new_name='StudentAccess',
        ),
        migrations.AddField(
            model_name='examtype',
            name='TeacherAccess',
            field=models.CharField(default='Declined', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exammarks',
            name='Marks',
            field=models.IntegerField(null=True),
        ),
    ]
