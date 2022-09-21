from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
PROFESSION = (
    (1, 'Doctor'),
    (2, 'Nurse'),
    (3, 'Physiotherapist'),
    (4, 'Dentist'),
    (5, 'Paramedic'),
)
DAY = ((1, 'Monday'),
       (2, 'Tuesday'),
       (3, 'Wednesday)'),
       (4, 'Thursday'),
       (5, 'Friday'),
       (6, 'Saturday'),
       (7, 'Sunday'),
       )


class MedUser(AbstractUser):
    PWZ = models.CharField(max_length=10)
    email = models.EmailField()
    profession = models.CharField(choices=PROFESSION, max_length=64)


class Patient(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    PESEL = models.CharField(max_length=11, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(MedUser, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=128)
    ICD_10 = models.CharField(max_length=128)
    symptoms = models.TextField()
    tests = models.TextField()
    imaging_examination = models.BooleanField(default=False)
    description_of_IE = models.TextField(blank=True)
    medicines = models.TextField(blank=True)
    medical_treatment = models.TextField(blank=True)
    home_recommendation = models.TextField(blank=True)


class Reservation(models.Model):
    owner = models.ForeignKey(MedUser, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time_of_reservation = models.DateTimeField()

    class Meta:
        unique_together = ('owner', 'time_of_reservation')


class Services(models.Model):
    owner = models.ForeignKey(MedUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()


class Location(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    workers_list = models.ManyToManyField(MedUser)


class WorkDay(models.Model):
    owner = models.ForeignKey(MedUser, on_delete=models.CASCADE)
    day = models.CharField(choices=DAY, max_length=24)
    start = models.TimeField()
    end = models.TimeField()
    interval = models.IntegerField(max_length=3)
