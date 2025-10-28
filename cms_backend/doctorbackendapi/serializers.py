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
    
    # Add these for better display
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    total_prescription_cost = serializers.SerializerMethodField()

    class Meta:
        model = Consultation
        fields = [
            'consultation_id', 'appointment', 'symptoms', 'notes', 'diagnosis',
            'prescriptions', 'lab_prescriptions', 'patient_name', 'doctor_name',
            'total_prescription_cost', 'created_at', 'updated_at'
        ]
        read_only_fields = ['consultation_id', 'created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        if obj.appointment and obj.appointment.patient:
            return f"{obj.appointment.patient.first_name} {obj.appointment.patient.last_name}"
        return "N/A"
    
    def get_doctor_name(self, obj):
        # FIXED: Use 'doc_id' instead of 'doctor'
        if obj.appointment and obj.appointment.doc_id:
            staff = obj.appointment.doc_id.Staff
            return f"Dr. {staff.FirstName} {staff.LastName}"
        return "N/A"
    
    def get_total_prescription_cost(self, obj):
        # Since prescriptions use CharField for medicine, we can't calculate cost directly
        # Return 0 or implement custom logic if needed
        return 0
