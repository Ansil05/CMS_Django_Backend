from rest_framework import generics
from .models import Labtest, Labrecord
from .serializers import LabtestSerializer, LabrecordSerializer
from Authentication.permissions import IsLabTechnician

class LabtestListCreateView(generics.ListCreateAPIView):
    queryset = Labtest.objects.all()
    serializer_class = LabtestSerializer
    # permission_classes = [IsLabTechnician]

class LabtestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Labtest.objects.all()
    serializer_class = LabtestSerializer
    # permission_classes = [IsLabTechnician]

class LabrecordListCreateView(generics.ListCreateAPIView):
    queryset = Labrecord.objects.all()
    serializer_class = LabrecordSerializer
    # permission_classes = [IsLabTechnician]

class LabrecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Labrecord.objects.all()
    serializer_class = LabrecordSerializer
    # permission_classes = [IsLabTechnician]