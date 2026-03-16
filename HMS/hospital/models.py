from django.db import models
from google_calendar import create_event
# Create your models here.

class doctor(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=100)
    prof_photo=models.ImageField(upload_to='doctors_photos/')
    exp=models.IntegerField(default=0)
    qualification=models.CharField(max_length=100)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class patient(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=20)

class appointment(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date} - {self.slot}"

