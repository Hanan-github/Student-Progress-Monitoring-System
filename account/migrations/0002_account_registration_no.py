# Generated by Django 4.0.3 on 2022-06-23 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='registration_no',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
