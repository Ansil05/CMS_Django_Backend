from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import permissions



class SignUpSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.AllowAny]
    role = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all(), message="Email already in use.")])
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password],style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True,required=True,style={'input_type': 'password'},label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        role = validated_data.pop('role')

        user = User.objects.create_user(password=password,**validated_data)

        if role:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        return user

class LoginSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.AllowAny]
    password = serializers.CharField(write_only = True, style={'input_type': 'password'})
    username = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username','password']
    
    