from rest_framework import serializers
from .models import Consultation, Prescription, LabPrescription
from labtechbackendapi.models import Labtest

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labtest
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class LabPrescriptionSerializer(serializers.ModelSerializer):
    testname = LabTestSerializer(read_only=True)
    testname_id = serializers.PrimaryKeyRelatedField(
        queryset=Labtest.objects.all(), source='testname', write_only=True
    )

    class Meta:
        model = LabPrescription
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    lab_prescriptions = LabPrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'