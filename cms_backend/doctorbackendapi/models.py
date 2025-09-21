from django.db import models
from reseptionistbackendapi.models import Appointment

class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="consultations")
    symptoms = models.TextField()
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField()

    def __str__(self):
        return f"Consultation {self.consultation_id} for Appointment {self.appointment.appointment_id}"


class Prescription(models.Model):
    pid = models.AutoField(primary_key=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="prescriptions")
    medicine = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return f"Prescription {self.pid} - {self.medicine}"


class LabPrescription(models.Model):
    lab_pid = models.AutoField(primary_key=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="lab_prescriptions")
    testname = models.CharField(max_length=200)

    def __str__(self):
        return f"Lab Test {self.testname} (#{self.lab_pid})"
