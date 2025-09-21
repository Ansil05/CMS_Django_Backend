
from rest_framework import viewsets
from .models import Patient, Appointment, ReceptionBill
from .serializers import PatientSerializer, AppointmentSerializer, ReceptionBillSerializer

class PatientViewSet(viewsets.ModelViewSet):
	queryset = Patient.objects.all()
	serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
	queryset = Appointment.objects.all()
	serializer_class = AppointmentSerializer

class ReceptionBillViewSet(viewsets.ModelViewSet):
	queryset = ReceptionBill.objects.all()
	serializer_class = ReceptionBillSerializer
