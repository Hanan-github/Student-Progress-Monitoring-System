# Generated by Django 4.0.4 on 2022-06-12 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='attendence',
        ),
        migrations.AlterField(
            model_name='parent',
            name='cnic',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
