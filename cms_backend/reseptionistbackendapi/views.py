
from rest_framework import viewsets
from .models import Patient, Appointment, ReceptionBill
from .serializers import PatientSerializer, AppointmentSerializer, ReceptionBillSerializer
from django.shortcuts import render
from Authentication.permissions import IsReceptionist
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [IsReceptionist]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doc_id').order_by('-created_at', '-appointment_date', '-appointment_time')
    serializer_class = AppointmentSerializer
    # permission_classes = [IsReceptionist]

class ReceptionBillViewSet(viewsets.ModelViewSet):
    queryset = ReceptionBill.objects.all()
    serializer_class = ReceptionBillSerializer
    # permission_classes = [IsReceptionist]

# Create your views here.
