from rest_framework import serializers
from .models import Consultation, Prescription, LabPrescription
from reseptionistbackendapi.models import Appointment, Patient
from labtechbackendapi.models import Labtest

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labtest
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        exclude = ['consultation']  # Do not require 'consultation' on nested create

class LabPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabPrescription
        exclude = ['consultation']

# Serializers for nested patient-in-appointment support
class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["Patient_id", "first_name", "last_name", "dob", "phone_no"]

class AppointmentSimpleSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "token_number",
            "appointment_date",
            "appointment_time",
            "created_at",
            "doc_id",
            "patient"
        ]

class ConsultationSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True)
    lab_prescriptions = LabPrescriptionSerializer(many=True)
    appointment = AppointmentSimpleSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'

    def create(self, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', [])
        lab_prescriptions_data = validated_data.pop('lab_prescriptions', [])
        appointment_id = self.initial_data.get('appointment')
        if appointment_id and not validated_data.get('appointment'):
            validated_data['appointment'] = Appointment.objects.get(pk=appointment_id)
        consultation = Consultation.objects.create(**validated_data)
        for pres_data in prescriptions_data:
            Prescription.objects.create(consultation=consultation, **pres_data)
        for lab_data in lab_prescriptions_data:
            LabPrescription.objects.create(consultation=consultation, **lab_data)
        return consultation
