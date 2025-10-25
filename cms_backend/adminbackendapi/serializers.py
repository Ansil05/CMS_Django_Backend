from rest_framework import serializers
from .models import Role, Specialization, Staff, Doctor
from datetime import date
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']  # You can add 'permissions' if needed



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

    def validate_RoleName(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Role name must be at least 3 characters long.")
        return value


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"

    def validate_SpecializationName(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Specialization name must be at least 3 characters long.")
        return value


class StaffSerializer(serializers.ModelSerializer):
    Role = RoleSerializer()

    class Meta:
        model = Staff
        fields = ["StaffId","FirstName", "LastName", "DOB", "PhoneNumber", "Gender", "Role", "Email", "Address", "PhoneNumber", "Address", "HireDate", "IsActive"]

    def validate_FirstName(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name should only contain letters.")
        return value

    def validate_LastName(self, value):
        if value and not value.isalpha():
            raise serializers.ValidationError("Last name should only contain letters.")
        return value

    def validate_DOB(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Staff must be at least 18 years old.")
        return value

    def validate_PhoneNumber(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits long.")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    Staff = StaffSerializer(read_only=True )
    Specialization = SpecializationSerializer(  read_only=True)

    class Meta:
        model = Doctor
        fields = ["Staff", "Specialization", "ConsultationFee", "availability", "YearsOfExperience"]

    def validate_ConsultationFee(self, value):
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative.")
        return value

    def validate_YearsOfExperience(self, value):
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        return value

    def validate(self, data):
        # Custom cross-field validation
        staff = data.get("Staff")
        specialization = data.get("Specialization")

        if Doctor.objects.filter(Staff=staff).exists() and self.instance is None:
            raise serializers.ValidationError("This staff member is already assigned as a doctor.")

        if staff.Role and staff.Role.RoleName.lower() != "doctor":
            raise serializers.ValidationError("Staff role must be 'Doctor' to be registered as a doctor.")

        return data
