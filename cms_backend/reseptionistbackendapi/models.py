
from django.db import models
from adminbackendapi.models import Doctor

# Patient model

from django.core.exceptions import ValidationError
from django.utils import timezone
import re
import datetime

class Patient(models.Model):
	BLOOD_GROUP_CHOICES = [
		('A+', 'A+'), ('A-', 'A-'),
		('B+', 'B+'), ('B-', 'B-'),
		('AB+', 'AB+'), ('AB-', 'AB-'),
		('O+', 'O+'), ('O-', 'O-'),
	]
	GENDER_CHOICES = [
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),
	]

	Patient_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	dob = models.DateField()
	blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
	phone_no = models.CharField(max_length=15, unique=True)
	address = models.TextField()
	email = models.EmailField(unique=True)
	reg_date = models.DateField(auto_now_add=True)

	def clean(self):
		# dob cannot be in future
		if self.dob > timezone.now().date():
			raise ValidationError({'dob': 'Date of birth cannot be in the future.'})
		# reg_date cannot be in future
		if self.dob and self.dob > datetime.date.today():
			raise ValidationError({'reg_date': 'Registration date cannot be in the future.'})
		# email validation (extra regex)
		email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
		if not re.match(email_regex, self.email):
			raise ValidationError({'email': 'Enter a valid email address.'})
		# phone number validation (10-15 digits, optional +)
		phone_regex = r'^\+?\d{10,15}$'
		if not re.match(phone_regex, self.phone_no):
			raise ValidationError({'phone_no': 'Enter a valid phone number (10-15 digits, optional +).'})

	def __str__(self):
		return f"{self.first_name} {self.last_name}"
	

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-Show', 'No-Show'),
    ]
    
    appointment_id = models.AutoField(primary_key=True)
    token_number = models.IntegerField(unique=True)
    doc_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')  # NEW
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  # NEW - NULLABLE

    def clean(self):
        today = timezone.now().date()
        if self.appointment_date < today:
            raise ValidationError({'appointment_date': 'Appointment date cannot be in the past.'})

    def save(self, *args, **kwargs):
        if not self.token_number:
            last_token = Appointment.objects.aggregate(models.Max('token_number'))['token_number__max'] or 0
            self.token_number = last_token + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_id} - {self.patient.first_name} {self.patient.last_name}"

    class Meta:
        ordering = ['-created_at', '-appointment_date', '-appointment_time']

# ReceptionBill model


class ReceptionBill(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('Cheque', 'Cheque'),
    ]
    
    bill_id = models.AutoField(primary_key=True)
    bill_number = models.CharField(max_length=50, unique=True, blank=True, null=True, editable=False)
    patient = models.ForeignKey(Patient, to_field='Patient_id', on_delete=models.CASCADE, related_name='bills')
    appointment = models.ForeignKey(Appointment, to_field='appointment_id', on_delete=models.CASCADE, related_name='bills')
    
    # Fee details
    reg_fee = models.DecimalField(max_digits=8, decimal_places=2)
    doc_fee = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Keep original name
    
    # NEW FIELDS - With proper defaults
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    payment_timestamp = models.DateTimeField(null=True, blank=True)  # NULLABLE - CRITICAL
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    bill_date = models.DateTimeField(null=True, blank=True)  # NULLABLE - CRITICAL
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  # NULLABLE - CRITICAL
    
    # Additional fields
    notes = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total
        self.total = self.reg_fee + self.doc_fee
        
        # Calculate balance
        if self.paid_amount is None:
            self.paid_amount = 0
        self.balance_amount = self.total - self.paid_amount
        
        # Auto-generate bill number if not exists
        if not self.bill_number:
            today = timezone.now()
            prefix = f"BILL{today.year}{today.month:02d}"
            last_bill = ReceptionBill.objects.filter(
                bill_number__startswith=prefix
            ).order_by('-bill_id').first()
            
            if last_bill and last_bill.bill_number:
                try:
                    last_seq = int(last_bill.bill_number[-4:])
                    new_seq = last_seq + 1
                except (ValueError, IndexError):
                    new_seq = 1
            else:
                new_seq = 1
            
            self.bill_number = f"{prefix}{new_seq:04d}"
        
        # Set bill_date if not set
        if not self.bill_date:
            self.bill_date = timezone.now()
        
        # Update payment status
        if self.paid_amount == 0:
            self.payment_status = 'PENDING'
        elif self.paid_amount >= self.total:
            self.payment_status = 'PAID'
        else:
            self.payment_status = 'PARTIAL'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill #{self.bill_number or self.bill_id} - {self.patient} - ₹{self.total}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reception Bill'
        verbose_name_plural = 'Reception Bills'
