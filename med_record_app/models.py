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


class MedUser(AbstractUser):
    PWZ = models.CharField(max_length=10)
    email = models.EmailField()
    profession = models.CharField(choices=PROFESSION, max_length=64)


class Patient(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    PESEL = models.CharField(max_length=11, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact = models.TextField(null=True, blank=True)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(MedUser, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=128)
    ICD_10 = models.CharField(max_length=128)
    symptoms = models.TextField()
    tests = models.TextField()
    imaging_examination = models.BooleanField(default=False)
    description_of_IE = models.TextField(null=True)
    medicines = models.TextField(null=True)
    medical_treatment = models.TextField(null=True)
    home_recommendation = models.TextField(null=True)


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
