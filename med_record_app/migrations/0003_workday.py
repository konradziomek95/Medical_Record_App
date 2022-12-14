# Generated by Django 4.1.1 on 2022-09-21 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('med_record_app', '0002_alter_patient_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday)'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], max_length=24)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('interval', models.IntegerField(max_length=3)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
