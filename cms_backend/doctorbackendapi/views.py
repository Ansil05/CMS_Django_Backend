from django.shortcuts import render
from Authentication.permissions import IsDoctor
# Create your views here.
from rest_framework import viewsets
from .models import Consultation, Prescription, LabPrescription
from labtechbackendapi.models import Labtest
from .serializers import (
    ConsultationSerializer,
    PrescriptionSerializer,
    LabPrescriptionSerializer,
    LabTestSerializer,
)

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    #permission_classes = [IsDoctor]

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    #permission_classes = [IsDoctor]

class LabPrescriptionViewSet(viewsets.ModelViewSet):
    queryset = LabPrescription.objects.all()
    serializer_class = LabPrescriptionSerializer
    # permission_classes = [IsDoctor]

class LabTestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Labtest.objects.all()
    serializer_class = LabTestSerializer
    # permission_classes = [IsDoctor]