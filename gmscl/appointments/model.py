from django.db import models


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    slot_time = models.TextField()
