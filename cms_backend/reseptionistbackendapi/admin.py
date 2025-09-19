from django.contrib import admin
from .models import Patient, Appointment, ReceptionBill

# Register your models here.
admin.register(Patient)
admin.register(Appointment)
admin.register(ReceptionBill)