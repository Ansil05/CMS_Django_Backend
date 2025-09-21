from django.contrib import admin

# Register your models here.
from .models import Consultation, Prescription, LabPrescription

admin.site.register(Consultation)
admin.site.register(Prescription)   
admin.site.register(LabPrescription)