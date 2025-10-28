
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
	


# Appointment model



class Appointment(models.Model):
	appointment_id = models.AutoField(primary_key=True)
	token_number = models.IntegerField(unique=True)
	doc_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
	appointment_date = models.DateField()
	appointment_time = models.TimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	def clean(self):
		# appointment_date cannot be in the past
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
	bill_id = models.AutoField(primary_key=True)
	patient = models.ForeignKey(Patient, to_field='Patient_id', on_delete=models.CASCADE, related_name='bills')
	appointment = models.ForeignKey(Appointment, to_field='appointment_id', on_delete=models.CASCADE, related_name='bills')
	reg_fee = models.DecimalField(max_digits=8, decimal_places=2)
	doc_fee = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
	total = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		# Fetch doc_fee from the related Doctor's ConsultationFee
		if self.appointment and self.appointment.doc_id:
			self.doc_fee = self.appointment.doc_id.ConsultationFee
		self.total = self.reg_fee + self.doc_fee
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Bill for {self.patient} (Appointment {self.appointment.appointment_id}) - Total: {self.total}" 

