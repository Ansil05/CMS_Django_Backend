from rest_framework import serializers
from .models import Labtest, Labrecord

class LabtestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labtest
        fields = '__all__'

class LabrecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labrecord
        fields = '__all__'