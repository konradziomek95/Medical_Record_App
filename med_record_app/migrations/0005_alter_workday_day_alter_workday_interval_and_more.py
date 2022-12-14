# Generated by Django 4.1.1 on 2022-09-22 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_record_app', '0004_alter_workday_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='day',
            field=models.CharField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], max_length=24),
        ),
        migrations.AlterField(
            model_name='workday',
            name='interval',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='workday',
            unique_together={('owner', 'day')},
        ),
    ]
