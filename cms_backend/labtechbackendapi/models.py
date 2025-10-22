from django.db import models
from reseptionistbackendapi. models import Patient
class Labtest(models.Model):
	test_id = models.AutoField(primary_key=True)
	test_name = models.CharField(max_length=255)
	description = models.TextField()
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	sample_required = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.test_name
      
class Labrecord(models.Model):
    rec_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True,) 
    test = models.ForeignKey(Labtest, on_delete=models.CASCADE, db_column='test_id')
    result = models.TextField()
    test_date = models.DateField()

    def __str__(self):
        return f"Record {self.rec_id} - Patient {self.patient_id}"

class LabTestRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(Labtest, on_delete=models.CASCADE)
    requested_date = models.DateField(auto_now_add=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Request {self.request_id} - {self.patient}"
    
class LabBill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(Labtest, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    test_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status_choices = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Insurance', 'Insurance'),
    ]
    payment_status = models.CharField(
        max_length=20, choices=payment_status_choices, default='Unpaid'
    )

    def __str__(self):
        return f"Bill {self.bill_id} - {self.patient}"

