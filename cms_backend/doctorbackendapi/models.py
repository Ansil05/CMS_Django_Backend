from django.db import models
from reseptionistbackendapi.models import Appointment, Patient
from pharmasistbackendapi.models import Medicine
from django.core.validators import MinValueValidator, MaxValueValidator



class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name="consultations"
    )
    symptoms = models.TextField()
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation {self.consultation_id} for Appointment {self.appointment.appointment_id}"
    
    @property
    def patient(self):
        """Get patient from appointment"""
        return self.appointment.patient if self.appointment else None

    class Meta:
        ordering = ['-created_at']


class Prescription(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Dispensing'),
        ('DISPENSED', 'Dispensed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    pid = models.AutoField(primary_key=True)
<<<<<<< HEAD
    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name="prescriptions"
    )
    medicine = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
=======
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="prescriptions")
    
    # UPDATED: Change from CharField to ForeignKey
    medicine = models.ForeignKey(
        Medicine, 
        on_delete=models.CASCADE,
        help_text="Medicine to prescribe"
    )
    
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg, 10ml")
    
    # ADD THESE NEW FIELDS
    frequency = models.CharField(
        max_length=100, 
        default="Twice daily",
        help_text="e.g., Twice daily, Every 6 hours"
    )
    duration = models.CharField(
        max_length=100, 
        default="5 days",
        help_text="e.g., 5 days, 2 weeks"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text="Number of units to dispense"
    )
    instructions = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Special instructions for this medicine"
    )
    before_food = models.BooleanField(default=False)
    after_food = models.BooleanField(default=False)
    
    # ADD STATUS FIELD
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)  # Add this
>>>>>>> teamperson

    def __str__(self):
        return f"Prescription {self.pid} - {self.medicine.name}"
    
    @property
    def total_cost(self):
        """Calculate total cost for this prescription item"""
        return self.quantity * self.medicine.unit_rate


class LabPrescription(models.Model):
    lab_pid = models.AutoField(primary_key=True)
    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name="lab_prescriptions"
    )
    testname = models.CharField(max_length=200)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lab Test {self.testname} (#{self.lab_pid})"
