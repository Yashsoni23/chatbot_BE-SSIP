from django import forms
from .model import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone_number',
                  'subject', 'description', 'slot_time']
