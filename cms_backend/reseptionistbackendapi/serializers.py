from rest_framework import serializers
from .models import Patient, Appointment, ReceptionBill

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['Patient_id', 'first_name', 'last_name', 'dob', 'phone_no', 'address', 'email', 'reg_date']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'token_number', 'doc_id', 'patient', 'appointment_date', 'appointment_time', 'created_at']

class ReceptionBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionBill
        fields = ['bill_id', 'patient', 'appointment', 'reg_fee', 'doc_fee', 'total', 'created_at']
