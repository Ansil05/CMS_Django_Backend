
# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from .models import Patient, Appointment, ReceptionBill
# from adminbackendapi.models import Doctor
# from django.utils import timezone

# class PatientAPITest(APITestCase):
# 	def setUp(self):
# 		self.patient_data = {
# 			"first_name": "John",
# 			"last_name": "Doe",
# 			"dob": "2000-01-01",
# 			"blood_group": "A+",
# 			"gender": "Male",
# 			"phone_no": "+911234567890",
# 			"address": "123 Street",
# 			"email": "john@example.com"
# 		}

# 	def test_create_patient(self):
# 		url = reverse('patient-list')
# 		response = self.client.post(url, self.patient_data, format='json')
# 		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# class AppointmentAPITest(APITestCase):
# 	def setUp(self):
# 		self.doctor = Doctor.objects.create(Staff_id=1, Specialization_id=1, ConsultationFee=500)
# 		self.patient = Patient.objects.create(
# 			first_name="Jane", last_name="Smith", dob="1995-05-05",
# 			blood_group="B+", gender="Female", phone_no="9876543210",
# 			address="456 Avenue", email="jane@example.com"
# 		)
# 		self.appointment_data = {
# 			"doc_id": self.doctor.pk,
# 			"patient": self.patient.pk,
# 			"appointment_date": (timezone.now() + timezone.timedelta(days=1)).isoformat()
# 		}

# 	def test_create_appointment(self):
# 		url = reverse('appointment-list')
# 		response = self.client.post(url, self.appointment_data, format='json')
# 		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# class ReceptionBillAPITest(APITestCase):
# 	def setUp(self):
# 		self.doctor = Doctor.objects.create(Staff_id=1, Specialization_id=1, ConsultationFee=500)
# 		self.patient = Patient.objects.create(
# 			first_name="Alice", last_name="Brown", dob="1990-10-10",
# 			blood_group="O+", gender="Female", phone_no="1234567890",
# 			address="789 Road", email="alice@example.com"
# 		)
# 		self.appointment = Appointment.objects.create(
# 			doc_id=self.doctor, patient=self.patient,
# 			appointment_date=(timezone.now() + timezone.timedelta(days=2))
# 		)
# 		self.bill_data = {
# 			"patient": self.patient.pk,
# 			"appointment": self.appointment.pk,
# 			"reg_fee": "100.00"
# 		}

# 	def test_create_bill(self):
# 		url = reverse('receptionbill-list')
# 		response = self.client.post(url, self.bill_data, format='json')
# 		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
