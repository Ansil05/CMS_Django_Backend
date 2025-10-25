from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
class Role(models.Model):
    RoleId = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=100)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.RoleName


class Specialization(models.Model):
    SpecializationId = models.AutoField(primary_key=True)
    SpecializationName = models.CharField(max_length=100, null=False, blank=False)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.SpecializationName

class Staff(models.Model):
    StaffId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100,null=False, blank=False)
    LastName = models.CharField(max_length=100)
    DOB = models.DateField(null=False, blank=False)
    Gender = models.CharField(max_length=10, choices=[('Male', 'male'), ('Female', 'female'), ('Other', 'other')])
    Role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    Email = models.EmailField(unique=True,null=False, blank=False)
    PhoneNumber = models.CharField(max_length=15, blank=False, null=False)
    Address = models.TextField(max_length=500, blank=False, null=False)
    HireDate = models.DateField(auto_now_add=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.FirstName + " " + self.LastName

class Doctor(models.Model):
    DoctorId = models.AutoField(primary_key=True)
    Staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    Specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    ConsultationFee = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=100,choices=[('Available', 'available'), ('Not Available', 'not available')], default='Available')
    YearsOfExperience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.Staff.FirstName} {self.Staff.LastName} - {self.Specialization.SpecializationName}"