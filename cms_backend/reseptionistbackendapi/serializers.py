from rest_framework import serializers
from .models import Patient, Appointment, ReceptionBill

class PatientSerializer(serializers.ModelSerializer):
    """Patient serializer"""
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'Patient_id', 'first_name', 'last_name', 'dob', 'age',
            'phone_no', 'address', 'email', 'blood_group', 'reg_date'
        ]
        read_only_fields = ['Patient_id', 'reg_date', 'age']


class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment serializer - FIXED to accept write operations"""
    
    # ✅ For reading: show patient details
    patient_name = serializers.SerializerMethodField(read_only=True)
    doctor_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'appointment_id', 'token_number',
            'patient', 'patient_name',
            'doc_id', 'doctor_name',
            'appointment_date', 'appointment_time',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['appointment_id', 'token_number', 'created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        """Get patient full name"""
        try:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        except:
            return "Unknown"
    
    def get_doctor_name(self, obj):
        """Get doctor name"""
        try:
            return f"Dr. {obj.doc_id.Staff.FirstName} {obj.doc_id.Staff.LastName}"
        except:
            return "Unknown Doctor"


class ReceptionBillSerializer(serializers.ModelSerializer):
    """Reception bill serializer"""
    
    # ✅ For reading: show patient name
    patient_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ReceptionBill
        fields = [
            'bill_id', 'bill_number',
            'patient', 'patient_name',
            'appointment',
            'reg_fee', 'doc_fee', 'total',
            'paid_amount', 'balance_amount',
            'payment_status', 'payment_mode',
            'payment_reference', 'payment_timestamp',
            'bill_date', 'created_at', 'updated_at',
            'notes', 'created_by'
        ]
        read_only_fields = ['bill_id', 'total', 'balance_amount', 'created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        """Get patient full name"""
        try:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        except:
            return "Unknown"
