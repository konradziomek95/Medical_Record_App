# Generated by Django 4.1.1 on 2022-09-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_record_app', '0003_workday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='interval',
            field=models.IntegerField(),
        ),
    ]
