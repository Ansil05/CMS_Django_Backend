
from django.db import models

# Patient model
class Patient(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	dob = models.DateField()
	blood_group = models.CharField(max_length=3)
	gender = models.CharField(max_length=10)
	phone_no = models.CharField(max_length=15, unique=True)
	address = models.TextField()
	email = models.EmailField(unique=True)
	reg_date = models.DateField(auto_now_add=True)
    #disaplay patient full name
	def __str__(self):
		return f"{self.first_name} {self.last_name}"
	


# Appointment model


class Appointment(models.Model):
	token_number = models.IntegerField(unique=True)
	doc_id = models.IntegerField()
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
	appointment_date = models.DateTimeField()
	appointment_time = models.TimeField()
	created_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if not self.token_number:
			last_token = Appointment.objects.aggregate(models.Max('token_number'))['token_number__max'] or 0
			self.token_number = last_token + 1
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Appointment for {self.patient} on {self.appointment_date} scheduled successfully with token {self.token_number}"

# ReceptionBill model
class ReceptionBill(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
	appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='bills')
	reg_fee = models.DecimalField(max_digits=8, decimal_places=2)
	doc_fee = models.DecimalField(max_digits=8, decimal_places=2)
	total = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		self.total = self.reg_fee + self.doc_fee
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Bill for {self.patient} (Appointment {self.appointment.id}) - Total: {self.total}" 

