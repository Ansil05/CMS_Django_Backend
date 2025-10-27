from rest_framework import serializers
from .models import Labtest, Labrecord,LabTestRequest,LabBill

class LabtestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labtest
        fields = '__all__'

class LabrecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labrecord
        fields = '__all__'

class LabTestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestRequest
        fields = '__all__'

class LabBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabBill
        fields = '__all__'