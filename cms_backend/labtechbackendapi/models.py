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
